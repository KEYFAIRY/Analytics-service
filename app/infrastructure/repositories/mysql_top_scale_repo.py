import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, TopScalesNotFoundException
from app.domain.entities.top_scale import TopScale
from app.domain.repositories.top_scale_repo import ITopScaleRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.top_scale_model import TopScaleModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLTopScaleRepository(ITopScaleRepository):

    async def get_top_scale(self, id_student: str, year: int, week: int) -> List[TopScale]:
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(TopScaleModel.id_student,
                           TopScaleModel.id_scale,
                           Scale.name.label('scale_name'),
                           TopScaleModel.fecha,
                           TopScaleModel.anio,
                           TopScaleModel.semana,
                           TopScaleModel.mes,
                           TopScaleModel.veces_practicada)
                    .join(Scale, Scale.id_scale == TopScaleModel.id_scale)
                    .where(
                        TopScaleModel.id_student == id_student,
                        TopScaleModel.anio == year,
                        TopScaleModel.semana == week)
                    .order_by(TopScaleModel.veces_practicada.desc())
                    .limit(3)  # Top 3
                )
                rows = query.fetchall()

                if not rows:
                    logger.warning(f"No top scales found for student {id_student}, year {year}, week {week}")
                    raise TopScalesNotFoundException()
                
                logger.debug(f"Top scales found: {rows}")
                return [self._row_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching top scales with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching top scales with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _row_to_entity(self, row) -> TopScale:
        return TopScale(
            id_student=row.id_student,
            id_scale=row.id_scale,
            scale=row.scale_name,
            date=row.fecha.strftime('%Y-%m-%d') if row.fecha else '',
            year=row.anio,
            week=row.semana,
            month=row.mes,
            times_practiced=row.veces_practicada
        )