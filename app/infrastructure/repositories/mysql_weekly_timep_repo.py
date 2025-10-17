import logging
from typing import List
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, WeeklyTimePostureNotFoundException
from app.domain.entities.weekly_time_posture import WeeklyTimePosture
from app.domain.repositories.weekly_timep_repo import IWeeklyTimePostureRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.weekly_timep_model import WeeklyPosturesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLWeeklyPostureRepository(IWeeklyTimePostureRepository):

    async def get_weekly_time_posture(self, id_student: str, year: int, week: int) -> List[WeeklyTimePosture]:
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name.label('scale_name'),
                           func.sum(WeeklyPosturesModel.tiempo_total).label('tiempo_total'),
                           func.sum(WeeklyPosturesModel.tiempo_mala_postura).label('tiempo_mala_postura'),
                           func.sum(WeeklyPosturesModel.tiempo_buena_postura).label('tiempo_buena_postura'))
                    .join(Scale, Scale.id == WeeklyPosturesModel.id_scale)
                    .where(
                        WeeklyPosturesModel.id_student == id_student,
                        WeeklyPosturesModel.anio == year,
                        WeeklyPosturesModel.semana == week)
                    .group_by(Scale.name)
                    .order_by(func.sum(WeeklyPosturesModel.tiempo_total).desc())
                )
                rows = query.fetchall()

                if not rows:
                    logger.warning(f"No weekly posture data found for student {id_student}, year {year}, week {week}")
                    raise WeeklyTimePostureNotFoundException()
                
                logger.debug(f"Weekly posture data found: {rows}")
                return [self._row_to_entity(row) for row in rows]
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching weekly posture data with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching weekly posture data with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
        
    def _row_to_entity(self, row) -> WeeklyTimePosture:
        return WeeklyTimePosture(
            scale=row.scale_name,
            time_practiced=float(row.tiempo_total) if row.tiempo_total else 0.0,
            bad_posture_time=float(row.tiempo_mala_postura) if row.tiempo_mala_postura else 0.0,
            good_posture_time=float(row.tiempo_buena_postura) if row.tiempo_buena_postura else 0.0
        )