from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os
import models  #SE HACE LA IMPORTACION DE MODELOS PARA QUE SQLModel LOS RECONOZCA
#SE DEFINE EL ARCHIVO DE LA BASE DE DATOS SQLITE
SQLITE_FILE_NAME = "database_sigmotoa_fc.db"
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(
    sqlite_url, echo=True, connect_args={"check_same_thread": False}
)
#FUNCIÓN PARA CREAR LAS TABLAS EN LA BASE DE DATOS
def create_db_and_tables():
    print(f"CREANDO LA BASES DE DATOS DE SIGMOTOA FC: {SQLITE_FILE_NAME}")
    SQLModel.metadata.create_all(engine)
#FUNCIÓN PARA DEVOLVER UNA SESIÓN SÍNCRONA DE LA BASE DE DATOS ESTO PARA DEPENDENCIAS EN FASTAPI
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        