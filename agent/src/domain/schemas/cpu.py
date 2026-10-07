"""
This module defines a data transfer model for a GetCpuResponseSchema.
"""
from pydantic import BaseModel


class GetCpuResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing CPU information.

    Attributes:
        id (int): The ID of the CPU data
        usage (str): The CPU usage in string format
    """

    id: int
    usage: str


class GetCpuCoreResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing CPU core number.

    Attributes:
        metric (str): name of the metric
        number (int): CPU core number
    """

    metric: str
    number: int

class GetAverageResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing CPU average value.

    Attributes:
        metric (str): name of the metric
        number (int): CPU average value
    """

    metric: str
    average_value: str