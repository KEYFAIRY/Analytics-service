from typing import List

from app.application.dto.top_scale_dto import TopScaleDTO
from app.domain.services.top_scale_service import TopScaleService

class GetTopScaleUseCase:
    def __init__(self, top_scale_service: TopScaleService):
        self.top_scale_service = top_scale_service

    async def execute(self, id_student: str, year: int, week: int) -> List[TopScaleDTO]:
        top_scales = await self.top_scale_service.get_top_scale(id_student, year, week)
        return [TopScaleDTO(
            id_student = scale.id_student,
            id_scale = scale.id_scale,
            date = scale.date,
            year = scale.year,
            week = scale.week,
            month = scale.month,
            times_practiced = scale.times_practiced
        ) for scale in top_scales]
