from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os
from models import Jugador, Partido, EstadisticaJugador

DATABASE_URL = "sqlite:///./sigmotoa.db"

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False
)

def create_db_and_tables():
    """Crea la base de datos y todas las tablas definidas en los modelos."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI para inyectar una sesión de base de datos
    en los endpoints. Cierra la sesión automáticamente al finalizar.
    """
    with Session(engine) as session:
        yield session