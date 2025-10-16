from typing import List

from app.application.dto.musical_mistakes_dto import MusicalMistakesDTO
from app.domain.services.musical_mistakes_service import MusicalMistakesService

class GetMusicalMistakesUseCase:
    def __init__(self, musical_mistakes_service: MusicalMistakesService):
        self.musical_mistakes_service = musical_mistakes_service

    async def execute(self, id_student: str, year: int, week: int) -> List[MusicalMistakesDTO]:
        musical_mistakes = await self.musical_mistakes_service.get_musical_mistakes(id_student, year, week)
        return [MusicalMistakesDTO(
            id_student = mistake.id_student,
            id_scale = mistake.id_scale,
            scale = mistake.scale,
            date = mistake.date,
            year = mistake.year,
            week = mistake.week,
            month = mistake.month,
            mistake_amount = mistake.mistake_amount
        ) for mistake in musical_mistakes]
