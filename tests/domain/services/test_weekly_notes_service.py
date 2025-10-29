import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.weekly_notes import WeeklyNotes
from app.domain.services.weekly_notes_service import WeeklyNotesService
from app.domain.repositories.weekly_notes_repo import IWeeklyNotesRepository

@pytest.fixture
def mock_weekly_notes_repo() -> IWeeklyNotesRepository:
    return AsyncMock(spec=IWeeklyNotesRepository)

@pytest.fixture
def weekly_notes_service(mock_weekly_notes_repo):
    return WeeklyNotesService(
        weekly_notes_repo=mock_weekly_notes_repo
    )

@pytest.fixture
def weekly_notes_1() -> WeeklyNotes:
    return WeeklyNotes(
        scale="C Major",
        right_notes=26,
        wrong_notes=3
    )

@pytest.fixture
def weekly_notes_2() -> WeeklyNotes:
    return WeeklyNotes(
        scale="G Major",
        right_notes=22,
        wrong_notes=7
    )

@pytest.fixture
def weekly_notes_3() -> WeeklyNotes:
    return WeeklyNotes(
        scale="D Minor",
        right_notes=27,
        wrong_notes=2
    )

class TestWeeklyNotesService:

    @pytest.mark.asyncio
    async def test_get_weekly_notes(self, weekly_notes_service, mock_weekly_notes_repo,
                                  weekly_notes_1, weekly_notes_2, weekly_notes_3):
        # Arrange
        mock_weekly_notes_repo.get_weekly_notes.return_value = [
            weekly_notes_1,
            weekly_notes_2,
            weekly_notes_3
        ]

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await weekly_notes_service.get_weekly_notes(id_student, year, week)

        # Assert
        assert result[0] == weekly_notes_1
        assert result[1] == weekly_notes_2
        assert result[2] == weekly_notes_3

    @pytest.mark.asyncio
    async def test_get_weekly_notes_none(self, weekly_notes_service, mock_weekly_notes_repo):
        # Arrange
        mock_weekly_notes_repo.get_weekly_notes.return_value = None

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await weekly_notes_service.get_weekly_notes(id_student, year, week)

        # Assert
        assert result is None