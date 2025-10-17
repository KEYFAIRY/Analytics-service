from dataclasses import dataclass

@dataclass
class WeeklyNotesDTO:
    scale: str
    right_notes: int
    wrong_notes: int