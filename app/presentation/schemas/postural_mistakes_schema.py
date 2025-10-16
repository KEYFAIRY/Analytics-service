from typing import List
from pydantic import BaseModel, Field

class PosturalMistakeItem(BaseModel):
    """Schema for each item in the list of postural mistakes"""

    escala: str = Field(..., description="Name of the musical scale", example="C Major")
    total_errores_posturales: int = Field(..., description="Amount of mistakes for the scale", example=2)
    dia: str = Field(..., description="Date of the record", example="2023-10-01")

class PosturalMistakesResponse(BaseModel):
    """Schema for postural mistakes response (list)"""
    data: List[PosturalMistakeItem] = Field(..., description = "List of postural mistakes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "escala": "C Major",
                        "total_errores_posturales": 2,
                        "dia": "2023-10-01"
                    },
                    {
                        "escala": "A minor",
                        "total_errores_posturales": 4,
                        "dia": "2023-10-02"
                    }
                ]
            }
        }