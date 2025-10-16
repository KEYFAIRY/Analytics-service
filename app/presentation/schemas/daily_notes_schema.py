from typing import List
from pydantic import BaseModel, Field

class DailyNotesItem(BaseModel):
    """Schema for each item in the list of daily notes"""

    escala: str = Field(..., description="Name of the musical scale", example="C Major")
    notas_correctas: int = Field(..., description="Amount of right notes played for the scale", example=10)
    notas_incorrectas: int = Field(..., description="Amount of wrong notes played for the scale", example=5)

class WeeklyNotesResponse(BaseModel):
    """Schema for weekly notes response (list)"""
    data: List[DailyNotesItem] = Field(..., description = "List of weekly notes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "escala": "C Major",
                        "notas_correctas": 10,
                        "notas_incorrectas": 5
                    },
                    {
                        "escala": "G Major",
                        "notas_correctas": 8,
                        "notas_incorrectas": 3
                    }
                ]
            }
        }