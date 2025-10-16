import logging
from typing import List
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, TopScalesNotFoundException
from app.domain.entities.top_scale import TopScale
from app.domain.repositories.top_scale_repo import ITopScaleRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.top_scale_model import TopScaleModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLTopScaleRepository(ITopScaleRepository):

    async def get_top_scale(self, id_student: str, year: int, week: int):
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name,
                           func.sum(TopScaleModel.times_practiced))
                    .join(Scale, Scale.id_scale == TopScaleModel.id_scale)
                    .where(
                        TopScaleModel.id_student == id_student,
                        TopScaleModel.year == year,
                        TopScaleModel.week == week)
                    .group_by(Scale.name)
                    .order_by(func.sum(TopScaleModel.times_practiced).desc())
                )
                rows = query.scalars().all()

                if not rows:
                    logger.warning(f"No top scales found for student {id_student}, year {year}, week {week}")
                    raise TopScalesNotFoundException()
                
                logger.debug(f"Top scales found: {rows}")
                return [self._model_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching top scales with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching top scales with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _model_to_entity(self, model: TopScaleModel) -> TopScale:
        return TopScale(
            id_student = model.id_student,
            id_scale = model.id_scale,
            date = model.date,
            year = model.year,
            week = model.week,
            month = model.month,
            times_practiced = model.times_practiced
        )