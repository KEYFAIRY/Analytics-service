import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.weekly_time_posture import WeeklyTimePosture
from app.domain.services.weekly_timep_service import WeeklyTimePostureService
from app.domain.repositories.weekly_timep_repo import IWeeklyTimePostureRepository

@pytest.fixture
def mock_weekly_timep_repo() -> IWeeklyTimePostureRepository:
    return AsyncMock(spec=IWeeklyTimePostureRepository)

@pytest.fixture
def weekly_time_posture_service(mock_weekly_timep_repo):
    return WeeklyTimePostureService(
        weekly_timep_repo=mock_weekly_timep_repo
    )

@pytest.fixture
def weekly_time_posture_1() -> WeeklyTimePosture:
    return WeeklyTimePosture(
        scale="C Major",
        time_practiced=120,
        bad_posture_time=15,
        good_posture_time=105
    )

@pytest.fixture
def weekly_time_posture_2() -> WeeklyTimePosture:
    return WeeklyTimePosture(
        scale="G Major",
        time_practiced=90,
        bad_posture_time=10,
        good_posture_time=80
    )

@pytest.fixture
def weekly_time_posture_3() -> WeeklyTimePosture:
    return WeeklyTimePosture(
        scale="D Minor",
        time_practiced=150,
        bad_posture_time=20,
        good_posture_time=130
    )

class TestWeeklyTimePostureService:

    @pytest.mark.asyncio
    async def test_get_weekly_time_posture(self, weekly_time_posture_service, mock_weekly_timep_repo,
                                  weekly_time_posture_1, weekly_time_posture_2, weekly_time_posture_3):
        # Arrange
        mock_weekly_timep_repo.get_weekly_time_posture.return_value = [
            weekly_time_posture_1,
            weekly_time_posture_2,
            weekly_time_posture_3
        ]

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await weekly_time_posture_service.get_weekly_time_posture(id_student, year, week)

        # Assert
        assert result[0] == weekly_time_posture_1
        assert result[1] == weekly_time_posture_2
        assert result[2] == weekly_time_posture_3

    @pytest.mark.asyncio
    async def test_get_weekly_time_posture_none(self, weekly_time_posture_service, mock_weekly_timep_repo):
        # Arrange
        mock_weekly_timep_repo.get_weekly_time_posture.return_value = None

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await weekly_time_posture_service.get_weekly_time_posture(id_student, year, week)

        # Assert
        assert result is None