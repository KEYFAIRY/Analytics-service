from typing import List

from app.application.dto.weekly_notes_dto import WeeklyNotesDTO
from app.domain.services.weekly_notes_service import WeeklyNotesService

class GetWeeklyNotesUseCase:
    def __init__(self, weekly_notes_service: WeeklyNotesService):
        self.weekly_notes_service = weekly_notes_service

    async def execute(self, id_student:str, year: int, week: int) -> List[WeeklyNotesDTO]:
        weekly_notes = await self.weekly_notes_service.get_weekly_notes(id_student, year, week)
        return [WeeklyNotesDTO(
            id_student = note.id_student,
            id_scale = note.id_scale,
            date = note.date,
            year = note.year,
            week = note.week,
            month = note.month,
            right_notes = note.right_notes,
            wrong_notes = note.wrong_notes
        ) for note in weekly_notes]