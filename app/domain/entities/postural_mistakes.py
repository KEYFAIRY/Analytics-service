from dataclasses import dataclass

@dataclass
class PosturalMistakes:
    id_student: str
    id_scale: int
    date: str
    year: int
    week: int
    month: int
    mistake_amount: int