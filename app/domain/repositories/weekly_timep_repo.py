from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.weekly_time_posture import WeeklyTimePosture

class IWeeklyTimePostureRepository(ABC):

    @abstractmethod
    async def get_weekly_time_posture(self, id_student: str, year: int, week: int) -> List[WeeklyTimePosture]:
        pass