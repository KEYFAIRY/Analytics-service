import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.musical_mistakes import MusicalMistakes
from app.domain.services.musical_mistakes_service import MusicalMistakesService
from app.domain.repositories.musical_mistakes_repo import IMusicalMistakesRepository

@pytest.fixture
def mock_musical_mistakes_repo() -> IMusicalMistakesRepository:
    return AsyncMock(spec=IMusicalMistakesRepository)

@pytest.fixture
def musical_mistakes_service(mock_musical_mistakes_repo):
    return MusicalMistakesService(
        musical_mistakes_repo=mock_musical_mistakes_repo
    )

@pytest.fixture
def musical_mistakes_1() -> MusicalMistakes:
    return MusicalMistakes(
        scale="C Major",
        date="2024-01-15",
        mistake_amount=5
    ) 

@pytest.fixture
def musical_mistakes_2() -> MusicalMistakes:
    return MusicalMistakes(
        scale="E Major",
        date="2024-01-16",
        mistake_amount=2
    ) 

@pytest.fixture
def musical_mistakes_3() -> MusicalMistakes:
    return MusicalMistakes(
        scale="A Major",
        date="2024-01-17",
        mistake_amount=7
    ) 

class TestMusicalMistakesService:

    @pytest.mark.asyncio
    async def test_get_musical_mistakes(self, musical_mistakes_service, mock_musical_mistakes_repo,
                                      musical_mistakes_1, musical_mistakes_2, musical_mistakes_3):
        # Arrange
        mock_musical_mistakes_repo.get_musical_mistakes.return_value = [
            musical_mistakes_1,
            musical_mistakes_2,
            musical_mistakes_3
        ]

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await musical_mistakes_service.get_musical_mistakes(id_student, year, week)

        # Assert
        assert result[0] == musical_mistakes_1
        assert result[1] == musical_mistakes_2
        assert result[2] == musical_mistakes_3

    @pytest.mark.asyncio
    async def test_get_musical_mistakes_none(self, musical_mistakes_service, mock_musical_mistakes_repo):
        # Arrange
        mock_musical_mistakes_repo.get_musical_mistakes.return_value = None

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await musical_mistakes_service.get_musical_mistakes(id_student, year, week)

        # Assert
        assert result is None