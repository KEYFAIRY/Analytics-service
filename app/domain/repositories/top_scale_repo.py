from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.top_scale import TopScale 

class ITopScaleRepository(ABC):

    @abstractmethod
    async def get_top_scales(self, id_student: str, year: int, week: int) -> List[TopScale]:
        pass