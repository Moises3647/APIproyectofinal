from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
import datetime

class SensorRegistro(Base):
    __tablename__ = "registros_s1"
    
    id = Column(Integer, primary_key=True, index=True)
    temperatura = Column(Float, nullable=False)
    humedad = Column(Float, nullable=False)
    foto_path = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # Puede ser 'admin' o 'device'