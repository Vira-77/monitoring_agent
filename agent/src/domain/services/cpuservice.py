"""
This module defines a controller class for fetching CPU values from a monitoring task.
"""
from typing import List
from domain.models import Cpu
from monitor import MonitorTask


# Controller class to fetch cpu values from monitoring task
class CpuService:
    """
    Controller class to fetch CPU values from a monitoring task.
    """

    def __init__(self: "CpuService")-> None:
        ...

    async def get_cpu(self: "CpuService", monitor_task: MonitorTask) -> List[Cpu]:
        """
        Get CPU values from the provided monitoring task and return them as a list of Cpu objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch CPU data from.

        Returns:
            List[Cpu]: A list of Cpu objects containing CPU values.
        """
        cpulist = []
        for core, usage in enumerate(monitor_task.cpu_percent):
            cpulist.append(Cpu(id=core, usage=str(usage)))
        return cpulist

    async def get_Average(self: "CpuService", monitor_task: MonitorTask) -> object:
        """
        Get Disk values from the provided monitoring task and return them as a list of Disk objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch Disk data from.

        Returns:
            List[Disk]: A list of Disk objects containing Disk values.
        """
        average_value = sum(monitor_task.cpu_percent) / len(monitor_task.cpu_percent)
        return {
            "metric": "averageuse",
            "average_value": str(average_value)
        }

    def __str__(self: "CpuService") -> str:
        """
        Return the string representation of the CpuService class.
        
        Returns:
            str: The name of the class.
        """
        return self.__class__.__name__
