import logging
from typing import List

from app.domain.entities.weekly_time_practice import WeeklyTimePractice
from app.domain.repositories.weekly_timep_repo import IWeeklyTimePracticeRepository

logger = logging.getLogger(__name__)

class WeeklyTimePracticeService:
    def __init__(self, weekly_timep_repo: IWeeklyTimePracticeRepository):
        self.weekly_timep_repo = weekly_timep_repo

    async def get_weekly_time_practice(self, id_student: str, year: int, week: int) -> List[WeeklyTimePractice]:
        logger.info(f"Fetching weekly time practice for student {id_student}, year {year}, week {week}")
        return await self.weekly_timep_repo.get_weekly_time_practice(id_student, year, week)