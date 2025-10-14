from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.postural_mistakes import PosturalMistakes

class IPosturalMistakesRepository(ABC):

    @abstractmethod
    async def get_postural_mistakes(self, id_student: str, year: int, week: int) -> List[PosturalMistakes]:
        pass