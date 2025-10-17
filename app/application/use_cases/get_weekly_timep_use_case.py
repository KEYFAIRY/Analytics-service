from typing import List

from app.application.dto.weekly_timep_dto import WeeklyTimePostureDTO
from app.domain.services.weekly_timep_service import WeeklyTimePostureService

class GetWeeklyTimePostureUseCase:
    def __init__(self, weekly_timep_service: WeeklyTimePostureService):
        self.weekly_timep_service = weekly_timep_service

    async def execute(self, id_student: str, year: int, week: int) -> List[WeeklyTimePostureDTO]:
        weekly_time_postures = await self.weekly_timep_service.get_weekly_time_posture(id_student, year, week)
        return [WeeklyTimePostureDTO(
            scale = posture.scale,
            time_practiced = posture.time_practiced,
            bad_posture_time = posture.bad_posture_time,
            good_posture_time = posture.good_posture_time
        ) for posture in weekly_time_postures]