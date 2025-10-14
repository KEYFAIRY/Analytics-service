from dataclasses import dataclass

@dataclass
class WeeklyNotes:
    id_student: str
    id_scale: int
    date: str
    year: int
    week: int
    month: int
    right_notes: int
    wrong_notes: int