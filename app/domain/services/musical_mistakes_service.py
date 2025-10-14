import logging
from typing import List

from app.domain.entities.musical_mistakes import MusicalMistakes
from app.domain.repositories.musical_mistakes_repo import IMusicalMistakesRepository

logger = logging.getLogger(__name__)

class MusicalMistakesService:
    def __init__(self, musical_mistakes_repo: IMusicalMistakesRepository):
        self.musical_mistakes_repo = musical_mistakes_repo

    async def get_musical_mistakes(self, id_student: str, year: int, week: int) -> List[MusicalMistakes]:
        logger.info(f"Fetching musical mistakes for student {id_student}, year {year}, week {week}")
        return await self.musical_mistakes_repo.get_musical_mistakes(id_student, year, week)