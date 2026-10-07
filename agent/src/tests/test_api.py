import threading
from fastapi.testclient import TestClient
from server import app
from monitor import MonitorTask
from collections import defaultdict
import re
from pathlib import Path

class MonitorTaskFake(MonitorTask):
    """
    Monitor class to mock the real monitor
    Instead of using the real monitor that fetch data on the host
    we use a monitor that provide "fake" values to control the output
    and make deterministic test (deterministic = repeatable and known values)
    """
    interval: int = 0
    cpu_percent: list[float] = ["10", "12"]
    num_cores: int = 3
    ram_metrics: dict = {
        "total": "10",
        "used": "5",
        "free": "5",
        "percent": "50",
    }
    disk_metrics: dict = {
        "total":"1000",
        "used": "50",
        "free": "9950",
        "percent": "0.1",
    }

    logs_metrics: list[object] = [{'status': '200', 'message': 'Request to /page1', 'error': '', 'timestamp': '09/Jan/2020:09:25:25 +0000', 'level': 'INFO', 'logger': 'HTTPAccess', 'method': 'GET'}, {'status': '200', 'message': 'Request to /page2', 'error': '', 'timestamp': '09/Jan/2020:12:12:49 +0000', 'level': 'INFO', 'logger': 'HTTPAccess', 'method': 'GET'}]
    status_counts = defaultdict(int)
    user_counts = defaultdict(int)
    error_count = 0
    access_log_path = Path(__file__).absolute().parent.parent.parent / 'test.log'
    wordpress_logs = [
        {'path': '/page1'},
        {'path': '/page1'},
        {'path': '/page2'}
    ]
    wordpress_error_logs = [
        {'status': '404', 'message': 'Request to /notfound', 'error': 'HTTP 404', 'timestamp': '09/Jan/2020:09:25:25 +0000', 'level': 'ERROR', 'logger': 'HTTPAccess', 'method': 'GET', 'path': '/notfound'},
        {'status': '500', 'message': 'Request to /servererror', 'error': 'HTTP 500', 'timestamp': '09/Jan/2020:12:12:49 +0000', 'level': 'ERROR', 'logger': 'HTTPAccess', 'method': 'POST', 'path': '/servererror'}
    ]

    def __init__(self: "MonitorTaskFake") -> None:
        pass

    def monitor(self: "MonitorTaskFake") -> None:
        pass

    def parse_log_line(self: "MonitorTask", line : str) -> dict:
        """
        Parse a single log line and extract relevant metrics.

        Args:
            line (str): The log line to parse.

        Returns:
            dict: A dictionary with parsed log data including status, message, timestamp, etc.
        """
        try:
            pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] "(?P<method>[A-Z]+) (?P<path>[^ ]*) (?P<protocol>HTTP/[\d.]+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)"'
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
                    'method': data['method']
                }
                
                self.status_counts[status] += 1
                self.user_counts[data['ip']] += 1
                self.wordpress_error_logs = [
                    {'status': '404', 'message': 'Request to /notfound', 'error': 'HTTP 404', 'timestamp': '09/Jan/2020:09:25:25 +0000', 'level': 'ERROR', 'logger': 'HTTPAccess', 'method': 'GET', 'path': '/notfound'},
                    {'status': '500', 'message': 'Request to /servererror', 'error': 'HTTP 500', 'timestamp': '09/Jan/2020:12:12:49 +0000', 'level': 'ERROR', 'logger': 'HTTPAccess', 'method': 'POST', 'path': '/servererror'}
                ]
                if status >= 400:
                    self.error_count += 1
                    
                return log_entry
        except Exception as e:
            print(f"Error parsing log line: {e}")
        return None

# Launching the real monitor for test involving the real monitor
client = TestClient(app)
thread = threading.Thread(target=app.state.monitortask.monitor, daemon=True)
thread.start()

def terminate_thread() -> None:
    """Terminate the background monitoring thread."""
    app.state.monitortask.isRunning = False
    thread.join(timeout=1) 

def test_server():
    response = client.get("/")
    assert response.status_code == 200

def test_default_route():
    response = client.get("/")
    print(response.json())
    assert response.json()["value"] == "Hello World"

def test_version_route():
    app.state.version = "1.0.0"
    response = client.get("/version")
    assert response.json()["value"] == "1.0.0"

def test_health() -> None:
    """
    Test the health endpoint to ensure the API is responsive.
    """
    response = client.get("/health")
    assert response.status_code == 200

def test_cpu_metrics():
    response = client.get("/metrics/v1/cpu")
    assert response.status_code == 200

def test_get_cpu_usage() -> None:
    """
    Test the CPU usage endpoint to verify the returned values match the expected "fake" CPU values.
    """
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [{"id": 0, "usage": "10"}, {"id": 1, "usage": "12"}]
    # restore monitortask for next test
    app.state.monitortask = save_app


def test_get_cpu_core() -> None:
    """
    Test the CPU core count endpoint to verify the returned value is as expected.
    """
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/cpu/core")
    # we can test types but not values because they will change at each test.
    assert response.status_code == 200
    assert response.json()["number"] == 3
    assert isinstance(response.json()["number"], int)
    #assert isinstance(response.json()["cores"], list)
    # restore monitortask for next test
    app.state.monitortask = save_app 

def test_disk_metrics():
    response = client.get("/metrics/v1/disk")
    assert response.status_code == 200
    # Add assertions to cover the missing lines

def test_get_disk_usage() -> None:
    """
    Test the disk usage endpoints for total, used, free, and percentage values.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/disk/total")
    assert response.status_code == 200
    assert response.json()["disk_value"] == "1000"
    assert isinstance(response.json()['disk_value'], str)
    app.state.monitortask = save_app

    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/disk/used")
    assert response.status_code == 200
    assert response.json()["disk_value"] == "50"
    assert isinstance(response.json()['disk_value'], str)
    app.state.monitortask = save_app

    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/disk/free")
    assert response.status_code == 200
    assert response.json()["disk_value"] == "9950"
    assert isinstance(response.json()['disk_value'], str)
    app.state.monitortask = save_app

    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/disk/percent")
    assert response.status_code == 200
    assert response.json()["disk_value"] == "0.1"
    assert isinstance(response.json()['disk_value'], str)
    app.state.monitortask = save_app
    
    
def test_get_memory_usage() -> None:
    """
    Test the RAM usage endpoints for total, used, free, and percentage values.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/ram/total")
    assert response.status_code == 200
    assert response.json()["value"] == '10'
    assert isinstance(response.json()["value"], str)

    response = client.get("/metrics/v1/ram/used")
    assert response.status_code == 200
    assert response.json()["value"] == '5'
    assert isinstance(response.json()["value"], str)

    response = client.get("/metrics/v1/ram/free")
    assert response.status_code == 200
    assert response.json()["value"] == '5'
    assert isinstance(response.json()["value"], str)

    response = client.get("/metrics/v1/ram/percent")
    assert response.status_code == 200
    assert response.json()["value"] == '50'
    assert isinstance(response.json()["value"], str)

    app.state.monitortask = save_app

    terminate_thread()


def test_parsing_log():
    """
    Test the parsing of log lines to ensure correct extraction of log details.
    """
    app.state.monitortask = MonitorTaskFake()
    log_line = '192.168.1.10 - - [01/Jan/2020:08:12:14 +0000] "GET / HTTP/1.1" 200 1245 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"'
    result = app.state.monitortask.parse_log_line(log_line)
    assert result["status"] == "200"
    assert result["message"] == "Request to /"
    assert result["error"] == ""
    assert result["timestamp"] == "01/Jan/2020:08:12:14 +0000"
    assert result["logger"] == "HTTPAccess"
    assert result["method"] == "GET"


def test_log_metrics():
    """
    Test the logs metrics endpoint to verify correct parsing and formatting of log data.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/logs/usage")
    assert response.status_code == 200
    assert response.json()[-2:] == [{'status': '200', 'message': 'Request to /page1', 'error': '', 'timestamp': '09/Jan/2020:09:25:25 +0000', 'level': 'INFO', 'logger': 'HTTPAccess', 'method': 'GET'}, {'status': '200', 'message': 'Request to /page2', 'error': '', 'timestamp': '09/Jan/2020:12:12:49 +0000', 'level': 'INFO', 'logger': 'HTTPAccess', 'method': 'GET'}]
    for res in response.json():
        assert isinstance(res["status"], str)
        assert isinstance(res["message"], str)
        assert isinstance(res["error"], str)
        assert isinstance(res["timestamp"], str)
        assert isinstance(res["logger"], str)
        assert isinstance(res["method"], str)
    app.state.monitortask = save_app

def test_get_most_viewed_page() -> None:
    """
    Test the most viewed page endpoint to verify the returned value is as expected.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/logs/most_viewed_page")
    assert response.status_code == 200
    assert "Most viewed page" in response.json()["value"]
    assert isinstance(response.json()["value"], str)
    app.state.monitortask = save_app

def test_get_last_errors() -> None:
    """
    Test the last errors endpoint to verify the returned values match the expected "fake" error logs.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()

    response = client.get("/metrics/v1/logs/last_errors")
    assert response.status_code == 200
    assert len(response.json()) == 2
    for res in response.json():
        assert isinstance(res["status"], str)
        assert isinstance(res["message"], str)
        assert isinstance(res["error"], str)
        assert isinstance(res["timestamp"], str)
        assert isinstance(res["level"], str)
        assert isinstance(res["logger"], str)
        assert isinstance(res["method"], str)
        assert isinstance(res["path"], str)
    app.state.monitortask = save_app

def test_get_top_processes() -> None:
    """
    Test the top processes endpoint to verify the returned values match the expected "fake" process data.
    """
    response = client.get("/metrics/v1/logs/topprocesses")
    assert response.status_code == 200
    for process in response.json():
        assert "name" in process
        assert "cpu_consumption" in process
        assert "ram_consumption" in process
        assert isinstance(process["name"], str)
        assert isinstance(process["cpu_consumption"], float)
        assert isinstance(process["ram_consumption"], float)

def test_get_cpu_name() -> None:
    """
    Test the CPU name endpoint to verify the returned value is as expected.
    """
    response = client.get("/metrics/v1/cpu/name")
    assert response.status_code == 200
    assert "name" in response.json()["metric"]
    assert isinstance(response.json()["average_value"], str)

def test_get_average_cpu_usage() -> None:
    """
    Test the average CPU usage endpoint to verify the returned value is as expected.
    """
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    app.state.monitortask.cpu_percent = [10, 12]
    response = client.get("/metrics/v1/cpu/averageuse")
    assert response.status_code == 200
    assert "averageuse" in response.json()[0]["metric"]
    app.state.monitortask = save_app