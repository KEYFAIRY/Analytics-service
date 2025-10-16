from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class WeeklyTimePosturesModel(Base):
    __tablename__ = "TiempoPosturasDiarias"

    id_student = Column("id_student", String(128), nullable=False, primary_key=True)
    id_scale = Column("id_scale", Integer, nullable=False, primary_key=True)
    date = Column("fecha", Date, nullable=False, primary_key=True)
    year = Column("anio", Integer, nullable=False)
    week = Column("semana", Integer, nullable=False)
    month = Column("mes", Integer, nullable=False)
    total_time = Column("tiempo_total", Float, nullable=False)
    bad_posture_time = Column("tiempo_mala_postura", Float, nullable=False)
    good_posture_time = Column("tiempo_buena_postura", Float, nullable=False)