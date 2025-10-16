import logging
from typing import List
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, PosturalMistakesNotFoundException
from app.domain.entities.postural_mistakes import PosturalMistakes
from app.domain.repositories.postural_mistakes_repo import IPosturalMistakesRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.postural_mistakes_model import PosturalMistakesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLPosturalMistakesRepository(IPosturalMistakesRepository):

    async def get_postural_mistakes(self, id_student, year, week):
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name,
                           func.sum(PosturalMistakesModel.mistake_amount))
                    .join(Scale, Scale.id_scale == PosturalMistakesModel.id_scale)
                    .where(
                        PosturalMistakesModel.id_student == id_student,
                        PosturalMistakesModel.year == year,
                        PosturalMistakesModel.week == week)
                    .group_by(Scale.name)
                )
                rows = query.scalars().all()

                if not rows:
                    logger. warning(f"No postural mistakes found for student {id_student}, year {year}, week {week}")
                    raise PosturalMistakesNotFoundException()
                
                logger.debug(f"Postural mistakes found: {rows}")
                return [self._model_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching postural mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching postural mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _model_to_entity(self, model: PosturalMistakesModel) -> PosturalMistakes:
        return PosturalMistakes(
            id_student = model.id_student,
            id_scale = model.id_scale,
            date = model.date,
            year = model.year,
            week = model.week,
            month = model.month,
            mistake_amount = model.mistake_amount
        )
