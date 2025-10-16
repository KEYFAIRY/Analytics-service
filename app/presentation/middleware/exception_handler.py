import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    AnalyticsServiceException,
    DatabaseConnectionException,
    ValidationException,
    MusicalMistakesNotFoundException,
    PosturalMistakesNotFoundException,
    TopScalesNotFoundException,
    WeeklyNotesNotFoundException,
    WeeklyTimePostureNotFoundException
)
from app.presentation.schemas.common_schema import StandardResponse


logger = logging.getLogger(__name__)

def build_response(exc: AnalyticsServiceException) -> dict:
    logger.error(str(exc))

    return StandardResponse(
        code=str(exc.code),
        message=exc.message,
        data=getattr(exc, 'details', None)
    ).dict()


async def analytics_service_exception_handler(request: Request, exc: AnalyticsServiceException):
    logger.error(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def musical_mistakes_not_found_exception_handler(request: Request, exc: MusicalMistakesNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def postural_mistakes_not_found_exception_handler(request: Request, exc: PosturalMistakesNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def top_scales_not_found_exception_handler(request: Request, exc: TopScalesNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def weekly_notes_not_found_exception_handler(request: Request, exc: WeeklyNotesNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def weekly_time_posture_not_found_exception_handler(request: Request, exc: WeeklyTimePostureNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def database_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    logger.error(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def validation_exception_handler(request: Request, exc: ValidationException):
    logger.warning(str(exc))
    return JSONResponse(status_code=int(exc.code), content=build_response(exc))

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Request validation error: {exc.errors()}")
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    formatted_message = "Validation errors: " + "; ".join(error_messages)
    response = StandardResponse.validation_error(formatted_message)
    return JSONResponse(status_code=422, content=response.dict())

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    response = StandardResponse.internal_error("An unexpected error occurred")
    return JSONResponse(status_code=500, content=response.dict())