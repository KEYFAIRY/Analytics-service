from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.weekly_notes import WeeklyNotes

class IWeeklyNotesRepository(ABC):

    @abstractmethod
    async def get_weekly_notes(self, id_student: str, year: int, week: int) -> List[WeeklyNotes]:
        pass