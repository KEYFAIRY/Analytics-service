from typing import List
from pydantic import BaseModel, Field

class TopScaleItem(BaseModel):
    """Schema for each item in the list of top scales"""

    name: str = Field(..., description="Name of the musical scale", example="C Major")
    times_practiced: int = Field(..., description="Number of times the scale was practiced", example=10)

class TopScaleResponse(BaseModel):
    """Schema for top scales response (list)"""
    items: List[TopScaleItem] = Field(..., description = "List of top scales", example = [])

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "C Major",
                        "times_practiced": 10
                    },
                    {
                        "name": "G Major",
                        "times_practiced": 8
                    }
                ]
            }
        }