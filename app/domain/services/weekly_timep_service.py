import logging
from typing import List

from app.domain.entities.weekly_time_posture import WeeklyTimePosture
from app.domain.repositories.weekly_timep_repo import IWeeklyTimePostureRepository

logger = logging.getLogger(__name__)

class WeeklyTimePostureService:
    def __init__(self, weekly_timep_repo: IWeeklyTimePostureRepository):
        self.weekly_timep_repo = weekly_timep_repo

    async def get_weekly_time_posture(self, id_student: str, year: int, week: int) -> List[WeeklyTimePosture]:
        logger.info(f"Fetching weekly time posture for student {id_student}, year {year}, week {week}")
        return await self.weekly_timep_repo.get_weekly_time_posture(id_student, year, week)