from dataclasses import dataclass

@dataclass
class MusicalMistakesDTO:
    scale: str
    date: str
    mistake_amount: int