import asyncio
import logging
from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exceptions import (
    AnalyticsServiceException,
    DatabaseConnectionException,
    MusicalMistakesNotFoundException,
    PosturalMistakesNotFoundException,
    TopScalesNotFoundException,
    ValidationException,
    WeeklyNotesNotFoundException,
    WeeklyTimePostureNotFoundException,
)
from app.infrastructure.database import mysql_connection
from app.presentation.api.v1.router import router as my_router
from app.presentation.middleware.exception_handler import (
    analytics_service_exception_handler,
    database_connection_exception_handler, 
    general_exception_handler,
    musical_mistakes_not_found_exception_handler,
    postural_mistakes_not_found_exception_handler,
    top_scales_not_found_exception_handler, 
    validation_exception_handler,
    weekly_notes_not_found_exception_handler,
    weekly_time_posture_not_found_exception_handler
)


# Configure logging
configure_logging()
logger = logging.getLogger(__name__)


async def initialize_databases(retry_delay: int = 5):
    mysql_connected = False
    attempt = 0
    
    while not (mysql_connected):
        logger.info(f"Reintentando conexión a BDs (intento {attempt + 1})...")
        await asyncio.sleep(retry_delay)
        
        attempt += 1
        
        # MySQL
        if not mysql_connected:
            try:
                mysql_connection.mysql_connection.init_engine()
                await mysql_connection.mysql_connection.verify_connection()
                mysql_connected = True
            except Exception as e:
                logger.warning(f"⚠️  MySQL connection failed: {e}")
    logger.info("✅ Todas las conexiones de BD establecidas y verificadas")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------- Startup ----------
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.APP_ENV}")

    # ---------- DB Connections ----------
    await initialize_databases(retry_delay=5)

    yield

    # ---------- Shutdown ----------
    await mysql_connection.mysql_connection.close_connections()
    logger.info("Database connections closed")


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(AnalyticsServiceException, analytics_service_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, database_connection_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(MusicalMistakesNotFoundException, musical_mistakes_not_found_exception_handler)
    app.add_exception_handler(PosturalMistakesNotFoundException, postural_mistakes_not_found_exception_handler)
    app.add_exception_handler(TopScalesNotFoundException, top_scales_not_found_exception_handler)
    app.add_exception_handler(WeeklyNotesNotFoundException, weekly_notes_not_found_exception_handler)
    app.add_exception_handler(WeeklyTimePostureNotFoundException, weekly_time_posture_not_found_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Health Check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    # Routers
    app.include_router(my_router)  # router is defined in presentation/api/v1

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.HOST}:{settings.ANALYTICS_SERVICE_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.ANALYTICS_SERVICE_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )