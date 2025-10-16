from dataclasses import dataclass

@dataclass
class WeeklyNotesDTO:
    id_student: str
    id_scale: int
    scale: str
    date: str
    year: int
    week: int
    month: int
    right_notes: int
    wrong_notes: int