from pydantic import BaseModel

class GetRamResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing RAM usage information.

    Attributes:
        metric (str): The name of the metric related to RAM usage (e.g., "RAM usage").
        value (str): The value of the metric, typically representing the amount of RAM used or available.
    """

    metric: str
    value: str
