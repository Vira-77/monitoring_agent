"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil
import threading
import re
from collections import defaultdict
from pathlib import Path

class MonitorTask:
    """A class for monitoring system and HTTP log metrics."""

    interval: int
    cpu_percent: list[float]
    num_cores: int
    isRunning: bool
    ram_metrics: dict
    disk_metrics: dict
    average_cores: list[float]  
    logs_metrics: list[dict]
    status_counts: defaultdict
    user_counts: defaultdict
    error_count: int
    access_log_path: Path

    def __init__(self: "MonitorTask") -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks.
        The monitoring interval is set to 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.cpu_percent = [0] * self.num_cores
        self.isRunning = True
        self.average_cores = [0]
        self.ram_metrics = {
            "total": 0,
            "used": 0,
            "free": 0,
            "percent": 0,
        }
        self.disk_metrics = {
            "total": 0,
            "used": 0,
            "free": 0,
            "percent": 0,
        }
        self.disk_percent = [0] * len(psutil.disk_partitions())
        self.logs_metrics = []  # List to hold parsed log entries
        self.status_counts = defaultdict(int)  # Count of each status code
        self.user_counts = defaultdict(int)  # Count of unique users
        self.error_count = 0  # Total error count
        self.wordpress_error_count = 0  # Total error count for WordPress logs
        self.wordpress_error_logs = []
        self.wordpress_logs = []
        self.access_log_path = Path(__file__).absolute().parent.parent.parent / 'agent.log'  # Path to the access log
        
        # Start monitoring in a separate thread
        time.sleep(self.interval)
        self.cpu_percent = psutil.cpu_percent(percpu=True)
        threading.Thread(name="monitor", target=self.monitor).start()

    def parse_log_line(self: "MonitorTask", line: str) -> dict:
        """
        Parse a single log line and extract relevant metrics.

        Args:
            line (str): The log line to parse.

        Returns:
            dict: A dictionary with parsed log data including status, message, timestamp, etc.
        """
        try:
            # Pattern for Apache log format (common log format)
            pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[\w:/]+) (?P<timezone>[+\-]\d{4})\] "(?P<method>[A-Z]+) (?P<path>[^ ]+) (?P<protocol>HTTP/[\d.]+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)"'
            match = re.match(pattern, line)
            
            if match:
                data = match.groupdict()
                status = int(data['status'])
                
                # Track the error count if status code >= 400
                if status >= 400:
                    self.error_count += 1

                log_entry = {
                    'status': str(status),
                    'message': f"Request to {data['path']}",
                    'error': '' if status < 400 else f"HTTP {status}",
                    'timestamp': data['timestamp'],
                    'level': 'ERROR' if status >= 400 else 'INFO',
                    'logger': 'HTTPAccess',
                    'method': data['method'],
                    'path': data['path'],  # Store the path for later analysis
                    'ip': data['ip']  # Store the IP address for user tracking
                }

                # Update status and user counts
                self.status_counts[status] += 1
                self.user_counts[data['ip']] += 1

                return log_entry
        except Exception as e:
            print(f"Error parsing log line: {e}")
        return None

    def process_logs(self: "MonitorTask") -> None:
        """
        Process the access log file and update metrics.

        This function reads the log file line by line, extracts useful information such as status codes, 
        timestamps, and request methods, and appends parsed log entries to the logs_metrics list.
        It also maintains counts of errors and user requests.
        """
        try:
            with open(self.access_log_path, 'r') as f:
                for line in f:
                    log_entry = self.parse_log_line(line.strip())
                    if log_entry:
                        self.logs_metrics.append(log_entry)
                        # Keep only the last 1000 entries
                        self.logs_metrics = self.logs_metrics[-1000:]
        except Exception as e:
            print(f"Error processing logs: {e}")

    def parse_wordpress_log_line(self: "MonitorTask", line: str) -> dict:
        """
        Parse a single log line and extract relevant metrics.

        Args:
            line (str): The log line to parse.

        Returns:
            dict: A dictionary with parsed log data including status, message, timestamp, etc.
        """
        try:
            # Pattern for Apache log format (common log format)
            pattern = r'^(?P<host>[\w\.-]+):(?P<port>\d{1,5}) (?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[\d\/\w\:\+\ ]+)\] "(?P<method>[A-Z]+) (?P<path>[^\s]+) (?P<protocol>HTTP\/[\d\.]+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^\"]*)" "(?P<useragent>[^\"]*)"'

            match = re.match(pattern, line)

            if match:
                data = match.groupdict()
                status = int(data['status'])

                log_entry = {
                    'status': str(status),
                    'message': f"Request to {data['path']}",
                    'error': '' if status < 400 else f"HTTP {status}",
                    'timestamp': data['timestamp'],
                    'level': 'ERROR' if status >= 400 else 'INFO',
                    'logger': 'HTTPAccess',
                    'method': data['method'],
                    'path': data['path'],
                    'ip': data['ip'],
                    'referrer': data.get('referrer', ''),
                    'useragent': data.get('useragent', ''),
                }

                unique_identifier = (log_entry['timestamp'], log_entry['method'], log_entry['path'], log_entry['status'])
            
                if not any((log['timestamp'], log['method'], log['path'], log['status']) == unique_identifier for log in self.wordpress_logs):
                    self.wordpress_logs.append(log_entry)
                
                    if status >= 400:
                        self.wordpress_error_count += 1
                        self.wordpress_error_logs.append(log_entry)
            
            return log_entry
        except Exception as e:
            print(f"Error parsing log line: {e}")
        return None

    def process_wordpress_logs(self: "MonitorTask") -> None:
        """
        Process the access log file and update metrics.

        This function reads the log file line by line, extracts useful information such as status codes, 
        timestamps, and request methods, and appends parsed log entries to the logs_metrics list.
        It also maintains counts of errors and user requests.
        """
        try:
            with open("/var/log/apache2/other_vhosts_access.log", 'r') as f:
                for line in f:
                    self.parse_wordpress_log_line(line.strip())
        except Exception as e:
            print(f"Error processing logs: {e}")
        
        self.wordpress_logs = self.wordpress_logs[-1000:]
        self.wordpress_error_logs = self.wordpress_error_logs[-5:]

    def monitor(self: "MonitorTask") -> None:
        """
        Continuously monitor and store the result in an attribute.

        This method runs in an infinite loop (while self.isRunning is True), collecting system metrics 
        (CPU usage, RAM usage, and disk usage) periodically, and updates the attributes accordingly. 
        It also processes the access logs regularly by calling process_logs().
        """
        while self.isRunning:
            # System metrics
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.virtual_memory = psutil.virtual_memory()
            self.ram_metrics["total"] = self.virtual_memory.total / (1024 ** 3)
            self.ram_metrics["used"] = self.virtual_memory.used / (1024 ** 3)
            self.ram_metrics["free"] = self.virtual_memory.free / (1024 ** 3)
            self.ram_metrics["percent"] = self.virtual_memory.percent
            self.average_cores = [sum(self.cpu_percent) / self.num_cores]

            self.disk_metrics["total"] = [
                psutil.disk_usage(part.mountpoint).total / (1024 ** 3)
                for part in psutil.disk_partitions()
            ]
            self.disk_metrics["used"] = [
                psutil.disk_usage(part.mountpoint).used / (1024 ** 3)
                for part in psutil.disk_partitions()
            ]
            self.disk_metrics["free"] = [
                psutil.disk_usage(part.mountpoint).free / (1024 ** 3)
                for part in psutil.disk_partitions()
            ]
            self.disk_metrics["percent"] = [
                psutil.disk_usage(part.mountpoint).percent
                for part in psutil.disk_partitions()
            ]

            self.process_logs()
            self.process_wordpress_logs()

            time.sleep(self.interval)

    def __str__(self: "MonitorTask") -> str:
        return f"MonitorTask(interval={self.interval})"
