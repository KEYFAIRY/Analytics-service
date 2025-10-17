from typing import List

from app.application.dto.musical_mistakes_dto import MusicalMistakesDTO
from app.domain.services.musical_mistakes_service import MusicalMistakesService

class GetMusicalMistakesUseCase:
    def __init__(self, musical_mistakes_service: MusicalMistakesService):
        self.musical_mistakes_service = musical_mistakes_service

    async def execute(self, id_student: str, year: int, week: int) -> List[MusicalMistakesDTO]:
        musical_mistakes = await self.musical_mistakes_service.get_musical_mistakes(id_student, year, week)
        return [MusicalMistakesDTO(
            scale = mistake.scale,
            date = mistake.date,
            mistake_amount = mistake.mistake_amount
        ) for mistake in musical_mistakes]
