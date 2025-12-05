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
    Partido,
    EstadisticaRead,
    EstadisticaReadWithPlayer,
    EstadisticaCreate,
    PartidoRead,
    PartidoCreate,
    PartidoReadWithPlayers,
    PartidoCreateWithPlayers,
    JugadorUpdate
)
#INICIALIZACIÓN DE LA APLICACIÓN FASTAPI
app = FastAPI(title="SIGMOTOA FÚTBOL CLUB", version="0.1.0", description="SISTEMA WEB PARA LA GESTIÓN DE DATOS DEL CLUB DE FÚTBOL SIGMOTOA FC")
#MONTAR LA CARPETA DE ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory="static"), name="static")
#CONFIGURACIÓN DE LOS TEMPLATES JINJA2
templates = Jinja2Templates(directory="templates")
#CONFIGURACIÓN DE SUPABASE
SUPABASE_URL: str = "https://okuotijfayaoecerimfi.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9rdW90aWpmYXlhb2VjZXJpbWZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ3OTg1OTMsImV4cCI6MjA4MDM3NDU5M30.8SstgKcCZs3CbcZSd0KEH4FQ7VBEnLR3t5RJeBzvsxk"
SUPABASE_BUCKET_NAME = "IMG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) #CREACIÓN DEL CLIENTE DE SUPABASE

#EJECUCIÓN DE LA CREACIÓN DE LA BASE DE DATOS Y TABLAS AL INICIAR EL SISTEMA WEB
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# RUTA BÁSICA: INICIO
@app.get("/", tags=["FRONTEND"])
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "SIGMOTOA FC - SISTEMA WEB DE GESTIÓN DE DATOS"})

# RUTA HTML: LISTADO DE JUGADORES
@app.get("/jugadores", response_class=HTMLResponse, tags=["FRONTEND"])
def listar_jugadores(request: Request, session: Session = Depends(get_session)):
    jugadores = session.exec(select(Jugador)).all()
    return templates.TemplateResponse(
        "jugadores.html",
        {
            "request": request,
            "jugadores": jugadores,
            "title": "Listado de Jugadores"
        }
    )




