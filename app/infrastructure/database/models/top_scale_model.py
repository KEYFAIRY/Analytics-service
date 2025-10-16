from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class TopScaleModel(Base):
    __tablename__ = "TopEscalasDiarias"

    id_student = Column("id_student",String(128), nullable=False, primary_key=True)
    id_scale = Column("id_scale", Integer, nullable=False, primary_key=True)
    date = Column("fecha",Date, nullable=False, primary_key=True)
    year = Column("anio", Integer, nullable=False)
    week = Column("semana", Integer, nullable=False)
    month = Column("mes", Integer, nullable=False)
    times_practiced = Column("veces_practicadas", Integer, nullable=False)
