from typing import List

from app.application.dto.top_scale_dto import TopScaleDTO
from app.domain.services.top_scale_service import TopScaleService

class GetTopScaleUseCase:
    def __init__(self, top_scale_service: TopScaleService):
        self.top_scale_service = top_scale_service

    async def execute(self, id_student: str, year: int, week: int) -> List[TopScaleDTO]:
        top_scales = await self.top_scale_service.get_top_scales(id_student, year, week)
        return [TopScaleDTO(
            scale = scale.scale,
            times_practiced = scale.times_practiced
        ) for scale in top_scales]
