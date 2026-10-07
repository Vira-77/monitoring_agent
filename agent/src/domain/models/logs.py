"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel


# Logs data model
class Logs(BaseModel):
    """
    Pydantic data model for representing Logs information.

    """

    status: str
    message: str
    error: str
    timestamp: str
    level: str
    logger: str
    method: str