import logging
from typing import List

from app.domain.entities.postural_mistakes import PosturalMistakes
from app.domain.repositories.postural_mistakes_repo import IPosturalMistakesRepository

logger = logging.getLogger(__name__)

class PosturalMistakesService:
    def __init__(self, postural_mistakes_repo: IPosturalMistakesRepository):
        self.postural_mistakes_repo = postural_mistakes_repo

    async def get_postural_mistakes(self, id_student: str, year: int, week: int) -> List[PosturalMistakes]:
        logger.info(f"Fetching postural mistakes for student {id_student}, year {year}, week {week}")
        return await self.postural_mistakes_repo.get_postural_mistakes(id_student, year, week)