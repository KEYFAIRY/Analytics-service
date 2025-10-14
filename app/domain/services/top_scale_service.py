import logging
from typing import List

from app.domain.entities.top_scale import TopScale
from app.domain.repositories.top_scale_repo import ITopScaleRepository

logger = logging.getLogger(__name__)

class TopScaleService:
    def __init__(self, top_scale_repo: ITopScaleRepository):
        self.top_scale_repo = top_scale_repo

    async def get_top_scale(self, id_student: str, year: int, week: int) -> List[TopScale]:
        logger.info(f"Fetching top scale for student {id_student}, year {year}, week {week}")
        return await self.top_scale_repo.get_top_scale(id_student, year, week)