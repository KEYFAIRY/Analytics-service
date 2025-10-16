from typing import List
from pydantic import BaseModel, Field

class DailyTimePostureItem(BaseModel):
    """Schema for each item in the list of daily time posture"""

    escala: str = Field(..., description="Name of the musical scale", example="C Major")
    tiempo_total_segundos: float = Field(..., description="Total time in seconds", example=36.2)
    tiempo_mala_postura_segundos: float= Field(..., description="Time in seconds spent in bad posture", example=12.5)
    tiempo_buena_postura_segundos: float = Field(..., description="Time in seconds spent in good posture", example=24.0)

class DailyTimePostureResponse(BaseModel):
    """Schema for daily time posture response (list)"""
    data: List[DailyTimePostureItem] = Field(..., description = "List of daily time posture", example = [])

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "escala": "C Major",
                        "tiempo_total_segundos": 36.2,
                        "tiempo_mala_postura_segundos": 12.5,
                        "tiempo_buena_postura_segundos": 24.0
                    },
                    {
                        "escala": "G Major",
                        "tiempo_total_segundos": 28.0,
                        "tiempo_mala_postura_segundos": 8.0,
                        "tiempo_buena_postura_segundos": 20.0
                    }
                ]
            }
        }