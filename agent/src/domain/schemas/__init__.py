from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema, GetAverageResponseSchema
from .ram import GetRamResponseSchema
from .disk import GetDiskResponseSchema
from .logs import GetLogsResponseSchema, ProcessResourceUsageSchema, GetLogsLastErrorResponseSchema

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
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetRamResponseSchema",
    "ExceptionResponseSchema",
    "GetDiskResponseSchema",
    "GetLogsResponseSchema",
    "GetAverageResponseSchema",
    "ProcessResourceUsageSchema",
    "BasicResponseSchema",
    "BasicIntResponseSchema",
    "GetLogsLastErrorResponseSchema"
]