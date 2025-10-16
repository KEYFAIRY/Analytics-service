from typing import List
from pydantic import BaseModel, Field

class MusicalMistakeItem(BaseModel):
    """Schema for each item in the list of musical mistakes"""

    escala: str = Field(..., description="Name of the musical scale", example="C Major")
    total_errores_musicales: int = Field(..., description="Amount of mistakes for the scale", example=5)
    dia: str = Field(..., description="Date of the record", example="2023-10-01")

class MusicalMistakesResponse(BaseModel):
    """Schema for musical mistakes response (list)"""
    data: List[MusicalMistakeItem] = Field(..., description = "List of musical mistakes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "escala": "C Major",
                        "total_errores_musicales": 5,
                        "dia": "2023-10-01"
                    },
                    {
                        "escala": "G Major",
                        "total_errores_musicales": 3,
                        "dia": "2023-10-02"
                    }
                ]
            }
        }
    