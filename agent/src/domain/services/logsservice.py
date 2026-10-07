"""
This module defines a controller class for fetching CPU values from a monitoring task.
"""
from typing import List
from domain.models import Logs
from monitor import MonitorTask
from datetime import datetime


# Controller class to fetch logs values from monitoring task
class LogsService:
    """
    Controller class to fetch CPU values from a monitoring task.
    """

    def __init__(self: "LogsService") -> None:
        ...

    async def get_logs(self: "LogsService", monitor_task: MonitorTask) -> List[Logs]:
        """
        Retrieve log metrics and statistics from the monitoring task.

        This function compiles a list of logs, including:
        - Overall statistics, such as total unique users and error counts.
        - The most recent log entries, limited to the last 100 entries.

        Args:
            monitor_task (MonitorTask): The monitoring task containing log and user data.

        Returns:
            List[Logs]: A list of Logs objects containing compiled log information.
        """
        logs_list = []
        
        # Add overall statistics
        logs_list.append(Logs(
            status="INFO",
            message=f"Total unique users: {len(monitor_task.user_counts)}",
            error="",
            timestamp=datetime.now().isoformat(),
            level="INFO",
            logger="Statistics",
            method="ANALYZE"
        ))
        
        logs_list.append(Logs(
            status="INFO",
            message=f"Total errors: {monitor_task.error_count}",
            error="",
            timestamp=datetime.now().isoformat(),
            level="INFO", 
            logger="Statistics",
            method="ANALYZE"
        ))

        # Add recent log entries
        for entry in monitor_task.logs_metrics[-100:]:  # Last 10 entries
            logs_list.append(Logs(status=entry['status'], message=entry['message'], error=entry['error'], timestamp=entry['timestamp'], level=entry['level'], logger=entry['logger'], method=entry['method']))
            
        return logs_list

    def __str__(self: "LogsService") -> str:
        """
        Return the string representation of the LogsService class.
        
        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__
