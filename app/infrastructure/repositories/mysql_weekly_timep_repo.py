import logging
from typing import List
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, WeeklyTimePostureNotFoundException
from app.domain.entities.weekly_time_posture import WeeklyTimePosture
from app.domain.repositories.weekly_timep_repo import IWeeklyTimePostureRepository
from app.infrastructure.database.mysql_connection import DatabaseConnection
from app.infrastructure.database.models.weekly_timep_model import WeeklyTimePosturesModel
from app.infrastructure.database.models.scale_model import Scale

logger = logging.getLogger(__name__)

class MySQLWeeklyTimePostureRepository(IWeeklyTimePostureRepository):

    async def get_weekly_time_posture(self, id_student, year, week):
        try:
            async with DatabaseConnection().get_async_session() as session:
                query = await session.execute(
                    select(Scale.name,
                           func.sum(WeeklyTimePosturesModel.total_time),
                           func.sum(WeeklyTimePosturesModel.bad_posture_time),
                           func.sum(WeeklyTimePosturesModel.good_posture_time))
                    .join(Scale, Scale.id_scale == WeeklyTimePosturesModel.id_scale)
                    .where(
                        WeeklyTimePosturesModel.id_student == id_student,
                        WeeklyTimePosturesModel.year == year,
                        WeeklyTimePosturesModel.week == week)
                    .group_by(Scale.name)
                    .order_by(func.sum(WeeklyTimePosturesModel.total_time).desc())
                )
                rows = query.scalars().all()

                if not rows:
                    logger.warning(f"No weekly time posture found for student {id_student}, year {year}, week {week}")
                    raise WeeklyTimePostureNotFoundException()
                
                logger.debug(f"Weekly time posture found: {rows}")
                return [self._model_to_entity(row) for row in rows]
        
        except IntegrityError as e:
            logger.error(f"MySQL integrity error while fetching weekly time posture with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Integrity error occurred while accessing the database.")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error while fetching weekly time posture with id_student {id_student}, year {year}, week {week}. Mistakes: {e}", exc_info=True)
            raise DatabaseConnectionException("Database error occurred while accessing the database.")
    
    def _model_to_entity(self, model: WeeklyTimePosturesModel) -> WeeklyTimePosture:
        return WeeklyTimePosture(
            id_student = model.id_student,
            id_scale = model.id_scale,
            date = model.date,
            year = model.year,
            week = model.week,
            month = model.month,
            total_time = model.total_time,
            bad_posture_time = model.bad_posture_time,
            good_posture_time = model.good_posture_time
        )