import logging
from typing import List
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, WeeklyNotesNotFoundException
from app.domain.entities.weekly_notes import WeeklyNotes
from app.domain.repositories.weekly_notes_repo import IWeeklyNotesRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.weekly_notes_model import WeeklyNotesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLWeeklyNotesRepository(IWeeklyNotesRepository):

    async def get_weekly_notes(self, id_student, year, week) -> List[WeeklyNotes]:
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name.label('scale_name'),
                           func.sum(WeeklyNotesModel.notas_correctas).label('notas_correctas'),
                           func.sum(WeeklyNotesModel.notas_incorrectas).label('notas_incorrectas'))
                    .join(Scale, Scale.id == WeeklyNotesModel.id_scale)
                    .where(
                        WeeklyNotesModel.id_student == id_student,
                        WeeklyNotesModel.anio == year,
                        WeeklyNotesModel.semana == week)
                    .group_by(Scale.name)
                    .order_by((func.sum(WeeklyNotesModel.notas_correctas)
                               + func.sum(WeeklyNotesModel.notas_incorrectas)).desc())
                )
                rows = query.fetchall()

                if not rows:
                    logger.warning(f"No weekly notes found for student {id_student}, year {year}, week {week}")
                    raise WeeklyNotesNotFoundException()
                
                logger.debug(f"Weekly notes found: {rows}")
                return [self._row_to_entity(row) for row in rows]
            
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching weekly notes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching weekly notes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _row_to_entity(self, row) -> WeeklyNotes:
        return WeeklyNotes(
            scale=row.scale_name,
            right_notes=row.notas_correctas,
            wrong_notes=row.notas_incorrectas
        )