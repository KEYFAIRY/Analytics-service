import logging
from fastapi import APIRouter, Depends, status
from typing import List

from app.application.use_cases.get_musical_mistakes_use_case import GetMusicalMistakesUseCase
from app.application.use_cases.get_postural_mistakes_use_case import GetPosturalMistakesUseCase
from app.application.use_cases.get_top_scale_use_case import GetTopScaleUseCase
from app.application.use_cases.get_weekly_notes_use_case import GetWeeklyNotesUseCase
from app.application.use_cases.get_weekly_timep_use_case import GetWeeklyTimePostureUseCase
from app.presentation.api.v1.dependencies import get_musical_mistakes_use_case_dependency
from app.presentation.api.v1.dependencies import get_postural_mistakes_use_case_dependency
from app.presentation.api.v1.dependencies import get_top_scale_use_case_dependency
from app.presentation.api.v1.dependencies import get_weekly_notes_use_case_dependency
from app.presentation.api.v1.dependencies import get_weekly_timep_use_case_dependency
from app.presentation.schemas.common_schema import StandardResponse
from app.presentation.schemas.musical_mistakes_schema import MusicalMistakeItem, MusicalMistakesResponse
from app.presentation.schemas.postural_mistakes_schema import PosturalMistakeItem, PosturalMistakesResponse
from app.presentation.schemas.top_scale_schema import TopScaleItem, TopScaleResponse
from app.presentation.schemas.weekly_notes_schema import WeeklyNotesItem, WeeklyNotesResponse
from app.presentation.schemas.weekly_time_posture_schema import WeeklyTimePostureItem, WeeklyTimePostureResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get(
    "/errores-musicales-semanales",
    response_model = StandardResponse[MusicalMistakesResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get weekly musical mistakes")
async def get_musical_mistakes(id_student:str, year:int, week:int,
                               use_case: GetMusicalMistakesUseCase = Depends(get_musical_mistakes_use_case_dependency)):
    # Endpoint that sends the musical mistakes for a student in a given week

    logger.info(f"Getting musical mistakes for student {id_student} in year {year}, week {week}")
    
    mistakes_dto : List = await use_case.execute(id_student, year, week)

    items = [
        MusicalMistakeItem(
            name=mistake.name,
            mistake_amount=mistake.mistake_amount
        ) for mistake in mistakes_dto
    ]

    response = MusicalMistakesResponse(items=items)

    return StandardResponse.success(data=response, message="Musical mistakes retrieved successfully")


@router.get(
    "/errores-posturales-semanales",
    response_model = StandardResponse[PosturalMistakesResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get weekly postural mistakes"
)
async def get_postural_mistakes(id_student: str, year: int, week: int,
                                use_case: GetPosturalMistakesUseCase = Depends(get_postural_mistakes_use_case_dependency)):
    
    # Endpoint that sends the postural mistakes for a student in a given week

    logger.info(f"Getting postural mistakes for student {id_student} in year {year}, week {week}")

    mistakes_dto: List = await use_case.execute(id_student, year, week)

    items = [
        PosturalMistakeItem(
            date=mistake.date,
            mistake_amount=mistake.mistake_amount
        ) for mistake in mistakes_dto
    ]

    response = PosturalMistakesResponse(items=items)

    return StandardResponse.success(data=response, message="Postural mistakes retrieved successfully")


@router.get(
    "/top-escalas-semanales",
    response_model = StandardResponse[TopScaleResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get top scales for a student in a given week"
)
async def get_top_scales(id_student: str, year: int, week: int,
                         use_case: GetTopScaleUseCase = Depends(get_top_scale_use_case_dependency)):
    
    # Endpoint that sends the top scales for a student in a given week

    logger.info(f"Getting top scales for student {id_student} in year {year}, week {week}")

    top_scales_dto: List = await use_case.execute(id_student, year, week)

    items = [
        TopScaleItem(
            name=scale.name,
            practice_time=scale.practice_time
        ) for scale in top_scales_dto
    ]

    response = TopScaleResponse(items=items)

    return StandardResponse.success(data=response, message="Top scales retrieved successfully")

@router.get(
    "/notas-resumen-semanales",
    response_model = StandardResponse,
    status_code = status.HTTP_200_OK,
    summary = "Get weekly notes summary"
)
async def get_weekly_notes(id_student: str, year: int, week: int,
                           use_case: GetWeeklyNotesUseCase = Depends(get_weekly_notes_use_case_dependency)):
    
    # Endpoint that sends the weekly notes summary for a student in a given week

    logger.info(f"Getting weekly notes summary for student {id_student} in year {year}, week {week}")

    notes_dto: List = await use_case.execute(id_student, year, week)

    items = [
        WeeklyNotesItem(
            date=note.date,
            average_note=note.average_note
        ) for note in notes_dto
    ]

    response = WeeklyNotesResponse(items=items)

    return StandardResponse.success(data=response, message="Weekly notes summary retrieved successfully")

@router.get(
    "/tiempo-posturas-semanales",
    response_model = StandardResponse,
    status_code = status.HTTP_200_OK,
    summary = "Get weekly time spent on postures"
)
async def get_weekly_time_posture(id_student: str, year: int, week: int,
                                  use_case: GetWeeklyTimePostureUseCase = Depends(get_weekly_timep_use_case_dependency)):
    
    # Endpoint that sends the weekly time spent on postures for a student in a given week

    logger.info(f"Getting weekly time spent on postures for student {id_student} in year {year}, week {week}")

    timep_dto: List = await use_case.execute(id_student, year, week)

    items = [
        WeeklyTimePostureItem(
            date=timep.date,
            time_spent=timep.time_spent
        ) for timep in timep_dto
    ]

    response = WeeklyTimePostureResponse(items=items)

    return StandardResponse.success(data=response, message="Weekly time spent on postures retrieved successfully")