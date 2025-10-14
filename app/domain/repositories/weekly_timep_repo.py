from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.weekly_time_practice import WeeklyTimePractice

class IWeeklyTimePracticeRepository(ABC):

    @abstractmethod
    async def get_weekly_time_practice(self, id_student: str, year: int, week: int) -> List[WeeklyTimePractice]:
        pass