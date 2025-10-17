from typing import List

from app.application.dto.weekly_notes_dto import WeeklyNotesDTO
from app.domain.services.weekly_notes_service import WeeklyNotesService

class GetWeeklyNotesUseCase:
    def __init__(self, weekly_notes_service: WeeklyNotesService):
        self.weekly_notes_service = weekly_notes_service

    async def execute(self, id_student:str, year: int, week: int) -> List[WeeklyNotesDTO]:
        weekly_notes = await self.weekly_notes_service.get_weekly_notes(id_student, year, week)
        return [WeeklyNotesDTO(
            scale = note.scale,
            right_notes = note.right_notes,
            wrong_notes = note.wrong_notes
        ) for note in weekly_notes]