from typing import List
from pydantic import BaseModel, Field

class WeeklyTimePostureItem(BaseModel):
    """Schema for each item in the list of weekly time posture"""

    name: str = Field(..., description="Name of the musical scale", example="C Major")
    total_time: float = Field(..., description="Total time in seconds", example=36.2)
    bad_posture_time: float= Field(..., description="Time in seconds spent in bad posture", example=12.5)
    good_posture_time: float = Field(..., description="Time in seconds spent in good posture", example=24.0)

class WeeklyTimePostureResponse(BaseModel):
    """Schema for weekly time posture response (list)"""
    items: List[WeeklyTimePostureItem] = Field(..., description = "List of weekly time posture", example = [])

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "C Major",
                        "total_time": 36.2,
                        "bad_posture_time": 12.5,
                        "good_posture_time": 24.0
                    },
                    {
                        "name": "G Major",
                        "total_time": 28.0,
                        "bad_posture_time": 8.0,
                        "good_posture_time": 20.0
                    }
                ]
            }
        }