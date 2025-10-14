import logging
from typing import List

from app.domain.entities.weekly_notes import WeeklyNotes
from app.domain.repositories.weekly_notes_repo import IWeeklyNotesRepository

logger = logging.getLogger(__name__)

class WeeklyNotesService:
    def __init__(self, weekly_notes_repo: IWeeklyNotesRepository):
        self.weekly_notes_repo = weekly_notes_repo

    async def get_weekly_notes(self, id_student: str, year: int, week: int) -> List[WeeklyNotes]:
        logger.info(f"Fetching weekly notes for student {id_student}, year {year}, week {week}")
        return await self.weekly_notes_repo.get_weekly_notes(id_student, year, week)