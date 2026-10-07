"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel


# CPU data model
class Cpu(BaseModel):

    id: int
    usage: str

# Average CPU data model
class Average(BaseModel):

    metric: str
    average_usage: str