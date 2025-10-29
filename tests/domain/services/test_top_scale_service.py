import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.top_scale import TopScale
from app.domain.services.top_scale_service import TopScaleService
from app.domain.repositories.top_scale_repo import ITopScaleRepository

@pytest.fixture
def mock_top_scale_repo() -> ITopScaleRepository:
    return AsyncMock(spec=ITopScaleRepository)

@pytest.fixture
def top_scale_service(mock_top_scale_repo):
    return TopScaleService(
        top_scale_repo=mock_top_scale_repo
    )

@pytest.fixture
def top_scale_1() -> TopScale:
    return TopScale(
        scale="C Major",
        times_practiced=10
    )

@pytest.fixture
def top_scale_2() -> TopScale:
    return TopScale(
        scale="G Major",
        times_practiced=8
    )

@pytest.fixture
def top_scale_3() -> TopScale:
    return TopScale(
        scale="D Minor",
        times_practiced=6
    )

class TestTopScaleService:

    @pytest.mark.asyncio
    async def test_get_top_scales(self, top_scale_service, mock_top_scale_repo,
                                 top_scale_1, top_scale_2, top_scale_3):
        # Arrange
        mock_top_scale_repo.get_top_scales.return_value = [
            top_scale_1,
            top_scale_2,
            top_scale_3
        ]

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await top_scale_service.get_top_scales(id_student, year, week)

        # Assert
        assert result[0] == top_scale_1
        assert result[1] == top_scale_2
        assert result[2] == top_scale_3

    @pytest.mark.asyncio
    async def test_get_top_scales_empty(self, top_scale_service, mock_top_scale_repo):
        # Arrange
        mock_top_scale_repo.get_top_scales.return_value = None

        # Act
        id_student = "123"
        year = 2024
        week = 3
        result = await top_scale_service.get_top_scales(id_student, year, week)

        # Assert
        assert result is None