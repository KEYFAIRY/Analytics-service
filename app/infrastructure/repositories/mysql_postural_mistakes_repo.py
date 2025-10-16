import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, PosturalMistakesNotFoundException
from app.domain.entities.postural_mistakes import PosturalMistakes
from app.domain.repositories.postural_mistakes_repo import IPosturalMistakesRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.postural_mistakes_model import PosturalMistakesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLPosturalMistakesRepository(IPosturalMistakesRepository):

    async def get_postural_mistakes(self, id_student, year, week) -> List[PosturalMistakes]:
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(PosturalMistakesModel.id_student,
                           PosturalMistakesModel.id_scale,
                           Scale.name.label('scale_name'),
                           PosturalMistakesModel.fecha,
                           PosturalMistakesModel.anio,
                           PosturalMistakesModel.semana,
                           PosturalMistakesModel.mes,
                           PosturalMistakesModel.cantidad_errores)
                    .join(Scale, Scale.id_scale == PosturalMistakesModel.id_scale)
                    .where(
                        PosturalMistakesModel.id_student == id_student,
                        PosturalMistakesModel.anio == year,
                        PosturalMistakesModel.semana == week)
                    .order_by(PosturalMistakesModel.cantidad_errores.desc())
                )
                rows = query.fetchall()

                if not rows:
                    logger.warning(f"No postural mistakes found for student {id_student}, year {year}, week {week}")
                    raise PosturalMistakesNotFoundException()
                
                logger.debug(f"Postural mistakes found: {rows}")
                return [self._row_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching postural mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching postural mistakes with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _row_to_entity(self, row) -> PosturalMistakes:
        return PosturalMistakes(
            id_student=row.id_student,
            id_scale=row.id_scale,
            scale=row.scale_name,
            date=row.fecha.strftime('%Y-%m-%d') if row.fecha else '',
            year=row.anio,
            week=row.semana,
            month=row.mes,
            mistake_amount=row.cantidad_errores
        )