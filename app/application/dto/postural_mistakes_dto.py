from dataclasses import dataclass

@dataclass
class PosturalMistakesDTO:
    scale: str
    date: str
    mistake_amount: int