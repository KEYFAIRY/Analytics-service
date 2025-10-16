from typing import List
from pydantic import BaseModel, Field

class MusicalMistakeItem(BaseModel):
    """Schema for each item in the list of musical mistakes"""

    name: str = Field(..., description="Name of the musical scale", example="C Major")
    mistake_amount: int = Field(..., description="Amount of mistakes for the scale", example=5)

class MusicalMistakesResponse(BaseModel):
    """Schema for musical mistakes response (list)"""
    items: List[MusicalMistakeItem] = Field(..., description = "List of musical mistakes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "C Major",
                        "mistake_amount": 5
                    },
                    {
                        "name": "G Major",
                        "mistake_amount": 3
                    }
                ]
            }
        }
    