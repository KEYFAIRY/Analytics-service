import logging
from typing import List
from sqlalchemy import func, select
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
                    select(Scale.name.label('scale_name'),
                           PosturalMistakesModel.fecha,
                           func.sum(PosturalMistakesModel.cantidad_errores).label('cantidad_errores'))
                    .join(Scale, Scale.id == PosturalMistakesModel.id_scale)
                    .where(
                        PosturalMistakesModel.id_student == id_student,
                        PosturalMistakesModel.anio == year,
                        PosturalMistakesModel.semana == week)
                    .group_by(Scale.name,
                              PosturalMistakesModel.fecha)
                    .order_by(PosturalMistakesModel.fecha.asc())
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
            scale=row.scale_name,
            date=row.fecha.strftime('%Y-%m-%d') if row.fecha else '',
            mistake_amount=row.cantidad_errores
        )