from typing import List

from app.application.dto.postural_mistakes_dto import PosturalMistakesDTO
from app.domain.services.postural_mistakes_service import PosturalMistakesService

class GetPosturalMistakesUseCase:
    def __init__(self, postural_mistakes_service: PosturalMistakesService):
        self.postural_mistakes_service = postural_mistakes_service

    async def execute(self, id_student: str, year: int, week: int) -> List[PosturalMistakesDTO]:
        postural_mistakes = await self.postural_mistakes_service.get_postural_mistakes(id_student, year, week)
        return [PosturalMistakesDTO(
            scale = mistake.scale,
            date = mistake.date,
            mistake_amount = mistake.mistake_amount
        ) for mistake in postural_mistakes]