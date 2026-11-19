from pydantic import BaseModel

from .cpu import (
    GetAverageResponseSchema,
    GetCpuCoreResponseSchema,
    GetCpuResponseSchema,
)
from .disk import GetDiskResponseSchema
from .logs import (
    GetLogsLastErrorResponseSchema,
    GetLogsResponseSchema,
    ProcessResourceUsageSchema,
)
from .ram import GetRamResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str

class BasicResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing basic information about a resource.

    Attributes:
        metric (str): The name of the metric related to the resource.
        value (str): The value of the metric.
    """

    metric: str
    value: str

class BasicIntResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing basic information about a resource.

    Attributes:
        metric (str): The name of the metric related to the resource.
        value (int): The value of the metric.
    """

    metric: str
    value: int

__all__ = [
    "BasicIntResponseSchema",
    "BasicResponseSchema",
    "ExceptionResponseSchema",
    "GetAverageResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetCpuResponseSchema",
    "GetDiskResponseSchema",
    "GetLogsLastErrorResponseSchema",
    "GetLogsResponseSchema",
    "GetRamResponseSchema",
    "ProcessResourceUsageSchema"
]