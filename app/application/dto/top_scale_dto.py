from dataclasses import dataclass

@dataclass
class TopScaleDTO:
    id_student: str
    id_scale: int
    scale: str
    date: str
    year: int
    week: int
    month: int
    times_practiced: int