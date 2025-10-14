from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.musical_mistakes import MusicalMistakes

class IMusicalMistakesRepository(ABC):

    @abstractmethod
    async def get_musical_mistakes(self, id_student: str, year: int, week: int) -> List[MusicalMistakes]:
        pass