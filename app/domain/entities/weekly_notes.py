from dataclasses import dataclass

@dataclass
class WeeklyNotes:
    scale: str
    right_notes: int
    wrong_notes: int