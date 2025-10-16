from typing import List
from pydantic import BaseModel, Field

class TopScaleItem(BaseModel):
    """Schema for each item in the list of top scales"""

    escala: str = Field(..., description="Name of the musical scale", example="C Major")
    veces_practicada: int = Field(..., description="Number of times the scale was practiced", example=10)

class TopScaleResponse(BaseModel):
    """Schema for top scales response (list)"""
    data: List[TopScaleItem] = Field(..., description = "List of top scales", example = [])

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "escala": "C Major",
                        "veces_practicada": 10
                    },
                    {
                        "escala": "G Major",
                        "veces_practicada": 8
                    }
                ]
            }
        }