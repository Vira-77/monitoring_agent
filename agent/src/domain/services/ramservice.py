"""
This module defines a controller class for fetching RAM values from a monitoring task.
"""
from typing import List
from domain.models import Ram
from monitor import MonitorTask


class RamService:
    """
    Controller class to fetch RAM values from a monitoring task.
    """

    def __init__(self: "RamService") -> None:
        ...

    async def get_ram(self: "RamService", monitor_task: MonitorTask) -> List[Ram]:
        """
        Get RAM usage values from the provided monitoring task and return them as a Ram object.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch RAM data from.

        Returns:
            Ram: An object containing RAM usage details.
        """
        ram_list = []
        for metric, value in monitor_task.ram_metrics.items():
            ram_list.append(Ram(metric=metric, value=str(value)))
        return ram_list

    def __str__(self: "RamService") -> str:
        """
        Return the string representation of the RamService class.
        
        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__
