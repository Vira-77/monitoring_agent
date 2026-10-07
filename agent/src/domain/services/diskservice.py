"""
This module defines a controller class for fetching Disk values from a monitoring task.
"""
from typing import List
from domain.models import Disk
from monitor import MonitorTask


# Controller class to fetch Disk values from monitoring task
class DiskService:
    """
    Controller class to fetch Disk values from a monitoring task.
    """

    def __init__(self: "DiskService") -> None:
        ...
    
    async def get_Disk(self: "DiskService", monitor_task: MonitorTask) -> List[Disk]:
        """
        Get RAM usage values from the provided monitoring task and return them as a Ram object.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch disk data from.

        Returns:
            Disk: An object containing Disk usage details.
        """
        disk_list = []
        for metric, disk_value in monitor_task.disk_metrics.items():
            disk_list.append(Disk(metric=metric, disk_value=str(disk_value)))
        return disk_list

    def __str__(self: "DiskService") -> str:
        """
        Return the string representation of the DiskService class.
        
        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__
