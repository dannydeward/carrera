from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    edad = Column(Integer)

    pais = Column(String)
    ciudad = Column(String)

    km_totales = Column(Float, default=0)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)


