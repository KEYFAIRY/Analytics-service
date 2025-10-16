import logging
from typing import List
from sqlalchemy import select
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
                    select(WeeklyNotesModel.id_student,
                           WeeklyNotesModel.id_scale,
                           Scale.name.label('scale_name'),
                           WeeklyNotesModel.fecha,
                           WeeklyNotesModel.anio,
                           WeeklyNotesModel.semana,
                           WeeklyNotesModel.mes,
                           WeeklyNotesModel.notas_correctas,
                           WeeklyNotesModel.notas_incorrectas)
                    .join(Scale, Scale.id == WeeklyNotesModel.id_scale)
                    .where(
                        WeeklyNotesModel.id_student == id_student,
                        WeeklyNotesModel.anio == year,
                        WeeklyNotesModel.semana == week)
                    .order_by(WeeklyNotesModel.notas_incorrectas.desc())
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
            id_student=row.id_student,
            id_scale=row.id_scale,
            scale=row.scale_name,
            date=row.fecha.strftime('%Y-%m-%d') if row.fecha else '',
            year=row.anio,
            week=row.semana,
            month=row.mes,
            right_notes=row.notas_correctas,
            wrong_notes=row.notas_incorrectas
        )