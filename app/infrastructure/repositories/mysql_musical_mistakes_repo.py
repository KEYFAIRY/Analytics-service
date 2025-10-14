import logging
from typing import List
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, MusicalMistakesNotFoundException
from app.domain.entities.musical_mistakes import MusicalMistakes
from app.domain.repositories.musical_mistakes_repo import IMusicalMistakesRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.musical_mistakes_model import MusicalMistakesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLMusicalMistakesRepository(IMusicalMistakesRepository):

    async def get_musical_mistakes(self, id_student, year, week) -> List[MusicalMistakes]:
        try:
            async with DatabaseConnection.get_async_session() as session:
                query = await session.execute(
                    select(Scale.name,
                            func.sum(MusicalMistakesModel.mistake_amount))
                    .join(Scale, Scale.id == MusicalMistakesModel.id_scale)
                    .where(
                            MusicalMistakesModel.id_student == id_student,
                            MusicalMistakesModel.year == year,
                            MusicalMistakesModel.week == week)
                    .group_by(Scale.name)
                )
                rows = query.scalars().all()

                if not rows:
                    logger.warning(f"No musical mistakes found for student {id_student}, year {year}, week {week}")
                    raise MusicalMistakesNotFoundException()
                
                logger.debug(f"Musical mistakes found: {rows}")
                return [self._model_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching musical with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching musical with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")

    def _model_to_entity(self, model: MusicalMistakesModel) -> MusicalMistakes:
        return MusicalMistakes(
            id_student = model.id_student,
            id_scale = model.id_scale,
            date = model.date,
            year = model.year,
            week = model.week,
            month = model.month,
            mistake_amount = model.mistake_amount
        )
