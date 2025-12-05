# database.py

from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os

# Importa todos los modelos para que SQLModel sepa qué tablas crear
from models import Jugador, Partido, EstadisticaJugador

# Configuración de la URL de la base de datos.
# Si estás usando Supabase/PostgreSQL, DEBES CAMBIAR ESTA LÍNEA
# con la URL de tu base de datos de producción.
DATABASE_URL = "sqlite:///./sigmotoa.db" # Usando SQLite para desarrollo local

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False # Mantiene la consola limpia. Cambia a True para ver las sentencias SQL.
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