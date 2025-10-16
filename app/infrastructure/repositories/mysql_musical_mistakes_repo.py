import logging
from typing import List
from sqlalchemy import select
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
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(MusicalMistakesModel.id_student,
                           MusicalMistakesModel.id_scale,
                           Scale.name.label('scale_name'),
                           MusicalMistakesModel.fecha,
                           MusicalMistakesModel.anio,
                           MusicalMistakesModel.semana,
                           MusicalMistakesModel.mes,
                           MusicalMistakesModel.cantidad_errores)
                    .join(Scale, Scale.id_scale == MusicalMistakesModel.id_scale)
                    .where(
                        MusicalMistakesModel.id_student == id_student,
                        MusicalMistakesModel.anio == year,
                        MusicalMistakesModel.semana == week)
                    .order_by(MusicalMistakesModel.cantidad_errores.desc())
                )
                rows = query.fetchall()

                if not rows:
                    logger.warning(f"No musical mistakes found for student {id_student}, year {year}, week {week}")
                    raise MusicalMistakesNotFoundException()
                
                logger.debug(f"Musical mistakes found: {rows}")
                return [self._row_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching musical mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching musical mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")

    def _row_to_entity(self, row) -> MusicalMistakes:
        return MusicalMistakes(
            id_student=row.id_student,
            id_scale=row.id_scale,
            scale=row.scale_name,
            date=row.fecha.strftime('%Y-%m-%d') if row.fecha else '',
            year=row.anio,
            week=row.semana,
            month=row.mes,
            mistake_amount=row.cantidad_errores
        )