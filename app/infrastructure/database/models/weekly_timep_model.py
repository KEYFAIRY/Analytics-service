from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class WeeklyTimePosturesModel(Base):
    __tablename__ = "TiempoPosturasDiarias"

    id_student = Column(String(128), nullable=False, primary_key=True)
    id_scale = Column(Integer, nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True)
    year = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    total_time = Column(Numeric, nullable=False)
    bad_posture_time = Column(Numeric, nullable=False)
    good_posture_time = Column(Numeric, nullable=False)