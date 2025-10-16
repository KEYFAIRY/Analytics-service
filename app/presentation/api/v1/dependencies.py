from functools import lru_cache

from app.application.use_cases.get_musical_mistakes_use_case import GetMusicalMistakesUseCase
from app.application.use_cases.get_postural_mistakes_use_case import GetPosturalMistakesUseCase
from app.application.use_cases.get_top_scale_use_case import GetTopScaleUseCase
from app.application.use_cases.get_weekly_notes_use_case import GetWeeklyNotesUseCase
from app.application.use_cases.get_weekly_timep_use_case import GetWeeklyTimePostureUseCase
from app.domain.services.musical_mistakes_service import MusicalMistakesService
from app.domain.services.postural_mistakes_service import PosturalMistakesService
from app.domain.services.top_scale_service import TopScaleService
from app.domain.services.weekly_notes_service import WeeklyNotesService
from app.domain.services.weekly_timep_service import WeeklyTimePostureService
from app.infrastructure.repositories.mysql_musical_mistakes_repo import MySQLMusicalMistakesRepository
from app.infrastructure.repositories.mysql_postural_mistakes_repo import MySQLPosturalMistakesRepository
from app.infrastructure.repositories.mysql_top_scale_repo import MySQLTopScaleRepository
from app.infrastructure.repositories.mysql_weekly_notes_repo import MySQLWeeklyNotesRepository
from app.infrastructure.repositories.mysql_weekly_timep_repo import MySQLWeeklyPostureRepository

# Repositories

@lru_cache
def get_mysql_top_scale_repository() -> MySQLTopScaleRepository:
    # Get an instance of MySQLTopScaleRepository
    return MySQLTopScaleRepository()

@lru_cache
def get_mysql_weekly_timep_repository() -> MySQLWeeklyPostureRepository:
    # Get an instance of MySQLWeeklyTimePostureRepository
    return MySQLWeeklyPostureRepository()

@lru_cache
def get_mysql_musical_mistakes_repository() -> MySQLMusicalMistakesRepository:
    # Get an instance of MySQLMusicalMistakesRepository
    return MySQLMusicalMistakesRepository()

@lru_cache
def get_mysql_postural_mistakes_repository() -> MySQLPosturalMistakesRepository:
    # Get an instance of MySQLPosturalMistakesRepository
    return MySQLPosturalMistakesRepository()

@lru_cache
def get_mysql_weekly_notes_repository() -> MySQLWeeklyNotesRepository:
    # Get an instance of MySQLWeeklyNotesRepository
    return MySQLWeeklyNotesRepository()



# Services

@lru_cache
def get_top_scale_service() -> TopScaleService:
    # Get an instance of TopScaleService
    return TopScaleService(top_scale_repo=get_mysql_top_scale_repository())

@lru_cache
def get_weekly_timep_service() -> WeeklyTimePostureService:
    # Get an instance of WeeklyTimePostureService
    return WeeklyTimePostureService(weekly_timep_repo=get_mysql_weekly_timep_repository())

@lru_cache
def get_musical_mistakes_service() -> MusicalMistakesService:
    # Get an instance of MusicalMistakesService
    return MusicalMistakesService(musical_mistakes_repo=get_mysql_musical_mistakes_repository())

@lru_cache
def get_postural_mistakes_service() -> PosturalMistakesService:
    # Get an instance of PosturalMistakesService
    return PosturalMistakesService(postural_mistakes_repo=get_mysql_postural_mistakes_repository())

@lru_cache
def get_weekly_notes_service() -> WeeklyNotesService:
    # Get an instance of WeeklyNotesService
    return WeeklyNotesService(weekly_notes_repo=get_mysql_weekly_notes_repository())



# Use Cases

@lru_cache
def get_top_scale_use_case() -> GetTopScaleUseCase:
    # Get an instance of GetTopScaleUseCase
    return GetTopScaleUseCase(top_scale_service=get_top_scale_service())

@lru_cache
def get_weekly_timep_use_case() -> GetWeeklyTimePostureUseCase:
    # Get an instance of GetWeeklyTimePostureUseCase
    return GetWeeklyTimePostureUseCase(weekly_timep_service=get_weekly_timep_service())

@lru_cache
def get_musical_mistakes_use_case() -> GetMusicalMistakesUseCase:
    # Get an instance of GetMusicalMistakesUseCase
    return GetMusicalMistakesUseCase(musical_mistakes_service=get_musical_mistakes_service())

@lru_cache
def get_postural_mistakes_use_case() -> GetPosturalMistakesUseCase:
    # Get an instance of GetPosturalMistakesUseCase
    return GetPosturalMistakesUseCase(postural_mistakes_service=get_postural_mistakes_service())

@lru_cache
def get_weekly_notes_use_case() -> GetWeeklyNotesUseCase:
    # Get an instance of GetWeeklyNotesUseCase
    return GetWeeklyNotesUseCase(weekly_notes_service=get_weekly_notes_service())



# Dependencies for FastAPI

def get_top_scale_use_case_dependency() -> GetTopScaleUseCase:
    # Dependency for injecting GetTopScaleUseCase
    return get_top_scale_use_case()

def get_weekly_timep_use_case_dependency() -> GetWeeklyTimePostureUseCase:
    # Dependency for injecting GetWeeklyTimePostureUseCase
    return get_weekly_timep_use_case()

def get_musical_mistakes_use_case_dependency() -> GetMusicalMistakesUseCase:
    # Dependency for injecting GetMusicalMistakesUseCase
    return get_musical_mistakes_use_case()

def get_postural_mistakes_use_case_dependency() -> GetPosturalMistakesUseCase:
    # Dependency for injecting GetPosturalMistakesUseCase
    return get_postural_mistakes_use_case() 

def get_weekly_notes_use_case_dependency() -> GetWeeklyNotesUseCase:
    # Dependency for injecting GetWeeklyNotesUseCase
    return get_weekly_notes_use_case()