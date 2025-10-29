import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.postural_mistakes import PosturalMistakes
from app.domain.services.postural_mistakes_service import PosturalMistakesService
from app.domain.repositories.postural_mistakes_repo import IPosturalMistakesRepository

@pytest.fixture
def mock_postural_mistakes_repo() -> IPosturalMistakesRepository:
    return AsyncMock(spec=IPosturalMistakesRepository)

@pytest.fixture
def postural_mistakes_service(mock_postural_mistakes_repo):
    return PosturalMistakesService(
        postural_mistakes_repo=mock_postural_mistakes_repo
    )

@pytest.fixture
def postural_mistakes_1() -> PosturalMistakes:
    return PosturalMistakes(
        scale="E Major",
        date="2024-01-15",
        mistake_amount=3
    )

@pytest.fixture
def postural_mistakes_2() -> PosturalMistakes:
    return PosturalMistakes(
        scale="A Minor",
        date="2024-01-16",
        mistake_amount=1
    )

@pytest.fixture
def postural_mistakes_3() -> PosturalMistakes:
    return PosturalMistakes(
        scale="D Major",
        date="2024-01-17",
        mistake_amount=4
    )

class TestPosturalMistakesService:

    @pytest.mark.asyncio
    async def test_get_postural_mistakes(self, postural_mistakes_service, mock_postural_mistakes_repo,
                                      postural_mistakes_1, postural_mistakes_2, postural_mistakes_3):
        # Arrange
        mock_postural_mistakes_repo.get_postural_mistakes.return_value = [
            postural_mistakes_1,
            postural_mistakes_2,
            postural_mistakes_3
        ]

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result =  await postural_mistakes_service.get_postural_mistakes(id_student, year, week)

        # Assert
        assert result[0] == postural_mistakes_1
        assert result[1] == postural_mistakes_2
        assert result[2] == postural_mistakes_3

    @pytest.mark.asyncio
    async def test_get_postural_mistakes_none(self, postural_mistakes_service, mock_postural_mistakes_repo):
        # Arrange
        mock_postural_mistakes_repo.get_postural_mistakes.return_value = None

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await postural_mistakes_service.get_postural_mistakes(id_student, year, week)

        # Assert
        assert result is None