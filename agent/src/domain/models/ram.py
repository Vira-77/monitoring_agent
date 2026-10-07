"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel

# RAM data model
class Ram(BaseModel):
    metric: str
    value: str
    