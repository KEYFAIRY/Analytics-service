import logging
from typing import List
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, WeeklyNotesNotFoundException
from app.domain.entities.weekly_notes import WeeklyNotes
from app.domain.repositories.weekly_notes_repo import IWeeklyNotesRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.weekly_notes_model import WeeklyNotesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLWeeklyNotesRepository(IWeeklyNotesRepository):

    async def get_weekly_notes(self, id_student, year, week):
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name,
                           func.sum(WeeklyNotesModel.right_notes),
                           func.sum(WeeklyNotesModel.wrong_notes))
                    .join(Scale, Scale.id_scale == WeeklyNotesModel.id_scale)
                    .where(
                        WeeklyNotesModel.id_student == id_student,
                        WeeklyNotesModel.year == year,
                        WeeklyNotesModel.week == week)
                    .group_by(Scale.name)
                    .order_by(func.sum(WeeklyNotesModel.wrong_notes).desc())
                )
                rows = query.scalars().all()

                if not rows:
                    logger.warning(f"No weekly notes found for student {id_student}, year {year}, week {week}")
                    raise WeeklyNotesNotFoundException()
                
                logger.debug(f"Weekly notes found: {rows}")
                return [self._model_to_entity(row) for row in rows]
            
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching weekly notes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching weekly notes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _model_to_entity(self, model: WeeklyNotesModel) -> WeeklyNotes:
        return WeeklyNotes(
            id_student = model.id_student,
            id_scale = model.id_scale,
            date = model.date,
            year = model.year,
            week = model.week,
            month = model.month,
            right_notes = model.right_notes,
            wrong_notes = model.wrong_notes
        )