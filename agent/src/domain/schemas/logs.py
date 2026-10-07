"""
This module defines a data transfer model for a GetCpuResponseSchema.
"""
from pydantic import BaseModel


class GetLogsResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing Logs information.

    Attributes:
        status (str): The status of the log retrieval operation (e.g., "success" or "failure").
        message (str): A descriptive message associated with the log entry.
        error (str): Details of any error encountered during log processing.
        timestamp (str): The timestamp indicating when the log entry was created.
        level (str): The severity level of the log (e.g., "INFO", "ERROR", "DEBUG").
        logger (str): The name of the logger that generated the log entry.
        method (str): The method or function associated with the log entry.
    """

    status: str
    message: str
    error: str
    timestamp: str
    level: str
    logger: str
    method: str

class GetLogsLastErrorResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing Logs information.

    Attributes:
        status (str): The status of the log retrieval operation (e.g., "success" or "failure").
        message (str): A descriptive message associated with the log entry.
        error (str): Details of any error encountered during log processing.
        timestamp (str): The timestamp indicating when the log entry was created.
        level (str): The severity level of the log (e.g., "INFO", "ERROR", "DEBUG").
        logger (str): The name of the logger that generated the log entry.
        method (str): The method or function associated with the log entry.
        path (str): The path or URL associated with the log entry.
    """

    status: str
    message: str
    error: str
    timestamp: str
    level: str
    logger: str
    method: str
    path: str

class ProcessResourceUsageSchema(BaseModel):
    name: str
    cpu_consumption: float 
    ram_consumption: float
