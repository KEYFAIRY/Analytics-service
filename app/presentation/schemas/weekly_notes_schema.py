from typing import List
from pydantic import BaseModel, Field

class WeeklyNotesItem(BaseModel):
    """Schema for each item in the list of weekly notes"""

    name: str = Field(..., description="Name of the musical scale", example="C Major")
    right_notes: int = Field(..., description="Amount of right notes played for the scale", example=10)
    wrong_notes: int = Field(..., description="Amount of wrong notes played for the scale", example=5)

class WeeklyNotesResponse(BaseModel):
    """Schema for weekly notes response (list)"""
    items: List[WeeklyNotesItem] = Field(..., description = "List of weekly notes", example = [])

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "C Major",
                        "right_notes": 10,
                        "wrong_notes": 5
                    },
                    {
                        "name": "G Major",
                        "right_notes": 8,
                        "wrong_notes": 3
                    }
                ]
            }
        }