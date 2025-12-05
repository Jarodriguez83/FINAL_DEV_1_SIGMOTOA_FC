#LIBERÍAS DE FASTAPI
from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException #FASTAPI PRINCIPAL
from fastapi.responses import HTMLResponse #RESPUESTAS HTML
#LIBRERÍAS DE BASE DE DATOS USO DE SUPABASE
from datetime import datetime
import shutil #MANEJO DE ARCHIVOS
from fastapi.params import Query
from httpx import request #PETICIONES HTTP
from sqlalchemy import or_ #OPERADORES LÓGICOS
from supabase import create_client, Client #CLIENTE DE SUPABASE
from starlette.requests import Request #PETICIONES HTTP
#LIBRERÍAS PARA EL USO DE TEMPLATES CON FASTAPI
from fastapi.templating import Jinja2Templates #TEMPLATES JINJA2
from fastapi.staticfiles import StaticFiles #ARCHIVOS ESTÁTICOS
#LIBERÍAS DE BASE DE DATOS USO DE SQLMODEL
from database import engine, get_session, create_db_and_tables
from sqlmodel import SQLModel, Session, select
from typing import List, Optional, Generator

#IMPORTACIÓN DE MODELOS Y MÓDULOS PROPIOS 
from models import (
    Jugador,
    JugadorCreate,
    JugadorRead,
    Estadistica,
    Partido 
)
#ESQUEMAS DE LECTURA ANIDACIÓN DE JUGADORES PARA MOSTRAR ESTADÍSTICAS
class EstadisticaRead(SQLModel):
    id: int
    total_tiempo_jugado_min: Optional[int] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    faltas_cometidas: Optional[int] = None
    suspensiones: Optional[bool] = None

    class Config:
        orm_mode = True
class EstadisticaReadWithPlayer(EstadisticaRead):
    jugador: Optional[JugadorRead] = None
class EstadisticaCreate(SQLModel):
    jugador_id: int
    total_tiempo_jugado_min: Optional[int] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    faltas_cometidas: Optional[int] = None
    suspensiones: Optional[bool] = None
class EstadisticaCreateWithPlayer(EstadisticaCreate):
    pass
class PartidoRead(SQLModel):
    id: int
    fecha_partido: datetime
    resultado: Optional[str] = None
    goles_sigmotoa: Optional[int] = None

    class Config:
        orm_mode = True
class PartidoCreate(SQLModel):
    fecha_partido: datetime
    resultado: Optional[str] = None
    goles_sigmotoa: Optional[int] = None
class PartidoReadWithPlayers(PartidoRead):
    jugadores: List[JugadorRead] = []
class PartidoCreateWithPlayers(PartidoCreate):
    jugadores: List[int] = []
class JugadorUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    posicion: Optional[str] = None
    numero_camiseta: Optional[int] = None
    edad: Optional[int] = None
    nacionalidad: Optional[str] = None



#INICIALIZACIÓN DE LA APLICACIÓN FASTAPI
app = FastAPI(title="SIGMOTOA FÚTBOL CLUB", version="0.1.0", description="SISTEMA WEB PARA LA GESTIÓN DE DATOS DEL CLUB DE FÚTBOL SIGMOTOA FC")
#MONTAR LA CARPETA DE ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory="static"), name="static")
#CONFIGURACIÓN DE LOS TEMPLATES JINJA2
templates = Jinja2Templates(directory="templates")
#CONFIGURACIÓN DE SUPABASE
SUPABASE_URL: str = "https://your-supabase-url.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
SUPABASE_BUCKET_NAME = "your-bucket-name"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) #CREACIÓN DEL CLIENTE DE SUPABASE
#EJECUCIÓN DE LA CREACIÓN DE LA BASE DE DATOS Y TABLAS AL INICIAR EL SISTEMA WEB 
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
#RUTAS BÁSICAS
@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}