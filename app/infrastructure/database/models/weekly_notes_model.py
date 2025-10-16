from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class WeeklyNotesModel(Base):
    __tablename__ = "NotasResumenDiarias"

    id_student = Column("id_student", String(128), nullable=False, primary_key=True)
    id_scale = Column("id_scale", Integer, nullable=False, primary_key=True)
    date = Column("fecha", Date, nullable=False, primary_key=True)
    year = Column("anio", Integer, nullable=False)
    week = Column("semana", Integer, nullable=False)
    month = Column("mes", Integer, nullable=False)
    right_notes = Column("notas_correctas", Integer, nullable=False)
    wrong_notes = Column("notas_incorrectas", Integer, nullable=False)