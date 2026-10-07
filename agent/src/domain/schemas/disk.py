"""
This module defines a data transfer model for a GetDiskResponseSchema.
"""
from pydantic import BaseModel


class GetDiskResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing Disk information.

    Attributes:
        metric (str): name of the metric
        number (int): Disk average value
    """

    metric: str
    disk_value: str