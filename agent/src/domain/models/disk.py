"""
This module defines a data model for Disk information.
"""
from pydantic import BaseModel



# Disk data model
class Disk(BaseModel):
    metric: str
    disk_value: str