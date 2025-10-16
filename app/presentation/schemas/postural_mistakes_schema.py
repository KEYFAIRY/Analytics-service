from typing import List
from pydantic import BaseModel, Field

class PosturalMistakeItem(BaseModel):
    """Schema for each item in the list of postural mistakes"""

    name: str = Field(..., description="Name of the musical scale", example="C Major")
    mistake_amount: int = Field(..., description="Amount of mistakes for the scale", example=2)

class PosturalMistakesResponse(BaseModel):
    """Schema for postural mistakes response (list)"""
    items: List[PosturalMistakeItem] = Field(..., description = "List of postural mistakes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "C Major",
                        "mistake_amount": 2
                    },
                    {
                        "name": "A minor",
                        "mistake_amount": 4
                    }
                ]
            }
        }