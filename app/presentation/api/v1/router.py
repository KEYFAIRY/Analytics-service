import logging
from fastapi import APIRouter, Depends, Query, status
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
    "/top-escalas-semanales",
    response_model = StandardResponse[TopScaleResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get top scales for a student in a given week"
)
async def get_top_scales(
    idStudent: str = Query(..., alias="idStudent"),
    anio: int = Query(..., alias="anio"),
    semana: int = Query(..., alias="semana"),
    use_case: GetTopScaleUseCase = Depends(get_top_scale_use_case_dependency)
):
    
    # Endpoint that sends the top scales for a student in a given week

    logger.info(f"Getting top scales for student {idStudent} in year {anio}, week {semana}")

    top_scales_dto = await use_case.execute(idStudent, anio, semana)

    items = [
        TopScaleItem(
            escala=scale.scale,
            veces_practicada=scale.times_practiced
        ) for scale in top_scales_dto
    ]

    response = TopScaleResponse(data=items)

    return StandardResponse.success(data=response, message="Top scales retrieved successfully")


@router.get(
    "/tiempo-posturas-semanales",
    response_model = StandardResponse,
    status_code = status.HTTP_200_OK,
    summary = "Get weekly time spent on postures"
)
async def get_weekly_time_posture(
    idStudent: str = Query(..., alias="idStudent"),
    anio: int = Query(..., alias="anio"),
    semana: int = Query(..., alias="semana"),
    use_case: GetWeeklyTimePostureUseCase = Depends(get_weekly_timep_use_case_dependency)
    ):
    
    # Endpoint that sends the weekly time spent on postures for a student in a given week

    logger.info(f"Getting weekly time spent on postures for student {idStudent} in year {anio}, week {semana}")

    weekly_posture = await use_case.execute(idStudent, anio, semana)

    items = [
        WeeklyTimePostureItem(
            escala=posture.scale,
            tiempo_total_segundos=posture.time_practiced,
            tiempo_mala_postura_segundos=posture.bad_posture_time,
            tiempo_buena_postura_segundos=posture.good_posture_time
        ) for posture in weekly_posture
    ]

    response = WeeklyTimePostureResponse(data=items)

    return StandardResponse.success(data=response, message="Weekly time spent on postures retrieved successfully")


@router.get(
    "/notas-resumen-semanales",
    response_model = StandardResponse,
    status_code = status.HTTP_200_OK,
    summary = "Get weekly notes summary"
)
async def get_weekly_notes(
    idStudent: str = Query(..., alias="idStudent"),
    anio: int = Query(..., alias="anio"),
    semana: int = Query(..., alias="semana"),
    use_case: GetWeeklyNotesUseCase = Depends(get_weekly_notes_use_case_dependency)
    ):
    
    # Endpoint that sends the weekly notes summary for a student in a given week

    logger.info(f"Getting weekly notes summary for student {idStudent} in year {anio}, week {semana}")

    notes_dto = await use_case.execute(idStudent, anio, semana)

    items = [
        WeeklyNotesItem(
            escala=note.scale,
            notas_correctas=note.right_notes,
            notas_incorrectas=note.wrong_notes
        ) for note in notes_dto
    ]

    response = WeeklyNotesResponse(data=items)

    return StandardResponse.success(data=response, message="Weekly notes summary retrieved successfully")


@router.get(
    "/errores-posturales-semanales",
    response_model = StandardResponse[PosturalMistakesResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get weekly postural mistakes"
)
async def get_postural_mistakes(
    idStudent: str = Query(..., alias="idStudent"),
    anio: int = Query(..., alias="anio"),
    semana: int = Query(..., alias="semana"),
    use_case: GetPosturalMistakesUseCase = Depends(get_postural_mistakes_use_case_dependency)
    ):
    
    # Endpoint that sends the postural mistakes for a student in a given week

    logger.info(f"Getting postural mistakes for student {idStudent} in year {anio}, week {semana}")

    mistakes_dto = await use_case.execute(idStudent, anio, semana)

    items = [
        PosturalMistakeItem(
            escala=mistake.scale,
            total_errores_posturales=mistake.mistake_amount,
            dia=mistake.date
        ) for mistake in mistakes_dto
    ]

    response = PosturalMistakesResponse(data=items)

    return StandardResponse.success(data=response, message="Postural mistakes retrieved successfully")


@router.get(
    "/errores-musicales-semanales",
    response_model = StandardResponse[MusicalMistakesResponse],
    status_code = status.HTTP_200_OK,
    summary = "Get weekly musical mistakes")
async def get_musical_mistakes(
    idStudent: str = Query(..., alias="idStudent"),
    anio: int = Query(..., alias="anio"),
    semana: int = Query(..., alias="semana"),
    use_case: GetMusicalMistakesUseCase = Depends(get_musical_mistakes_use_case_dependency)
    ):
    # Endpoint that sends the musical mistakes for a student in a given week

    logger.info(f"Getting musical mistakes for student {idStudent} in year {anio}, week {semana}")

    mistakes_dto = await use_case.execute(idStudent, anio, semana)

    items = [
        MusicalMistakeItem(
            escala=mistake.scale,
            total_errores_musicales=mistake.mistake_amount,
            dia=mistake.date
        ) for mistake in mistakes_dto
    ]

    response = MusicalMistakesResponse(data=items)

    return StandardResponse.success(data=response, message="Musical mistakes retrieved successfully")