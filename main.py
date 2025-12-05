from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from sqlmodel import Session, select
from typing import Optional
from models import Jugador, Partido, PosicionEnum, PieDominanteEnum, EstadoJugadorEnum
from database import engine, get_session, create_db_and_tables
app = FastAPI(title="SIGMOTOA FÚTBOL CLUB", version="0.1.0",
              description="SISTEMA WEB PARA LA GESTIÓN DE DATOS DEL CLUB DE FÚTBOL SIGMOTOA FC")

# CONFIGURACIÓN DE LOS TEMPLATES Y ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

templates.env.globals['now'] = datetime.now

@app.on_event("startup")
def on_startup():
    """Ejecuta la creación de tablas al iniciar el servidor."""
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    """Página de inicio"""
    return templates.TemplateResponse("index.html", {"request": request})


# --- ENDPOINTS JUGADORES ---
@app.get("/jugadores", response_class=HTMLResponse)
def read_jugadores(request: Request, session: Session = Depends(get_session)):
    """Muestra la lista de jugadores y el formulario."""
    try:
        jugadores = session.exec(select(Jugador)).all()
    except Exception as e:
        # Esto captura errores de DB si no se han creado las tablas correctamente
        print(f"Error al cargar jugadores: {e}")
        jugadores = []

    context = {
        "request": request,
        "jugadores": jugadores,
        # Se envían los valores de los Enums
        "posiciones": [p.value for p in PosicionEnum],
        "pies_dominantes": [p.value for p in PieDominanteEnum],
        "estados": [e.value for e in EstadoJugadorEnum],
    }
    return templates.TemplateResponse("jugadores.html", context)


@app.post("/jugadores")
def create_jugador(
        nombre: str = Form(...),
        numero_camiseta: int = Form(...),
        fecha_nacimiento: str = Form(...),
        nacionalidad: str = Form(...),
        fotografia_url: Optional[str] = Form(None),  # Solución con Optional importado
        altura_cm: int = Form(...),
        peso_kg: int = Form(...),

        pie_dominante_str: str = Form(..., alias="pie_dominante"),
        posicion_str: str = Form(..., alias="posicion"),

        ano_ingreso_club: int = Form(...),
        valor_mercado_col: int = Form(...),

        estado_jugador_str: str = Form(..., alias="estado_jugador"),

        session: Session = Depends(get_session)
):
    """Crea un nuevo jugador en la DB."""
    try:
        new_player = Jugador(
            nombre=nombre,
            numero_camiseta=numero_camiseta,
            # Conversión explícita a date
            fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
            nacionalidad=nacionalidad,
            fotografia_url=fotografia_url,
            altura_cm=altura_cm,
            peso_kg=peso_kg,
            # Conversión explícita a Enum
            pie_dominante=PieDominanteEnum(pie_dominante_str),
            posicion=PosicionEnum(posicion_str),

            ano_ingreso_club=ano_ingreso_club,
            valor_mercado_col=valor_mercado_col,

            estado_jugador=EstadoJugadorEnum(estado_jugador_str)
        )
        session.add(new_player)
        session.commit()
        session.refresh(new_player)
        return RedirectResponse("/jugadores", status_code=303)
    except ValueError as e:
        # Error si el string no es un Enum válido o hay error de formato de fecha
        raise HTTPException(status_code=400,
                            detail=f"Error en el valor proporcionado: {e}. Verifique que las selecciones sean correctas y el formato de fecha sea YYYY-MM-DD.")
    except Exception as e:
        # Error general, ej. número de camiseta duplicado, restricción violada
        raise HTTPException(status_code=400,
                            detail=f"Error al crear el jugador (Posible duplicado o valor fuera de rango): {e}")


# --- ENDPOINTS PARTIDOS ---

@app.get("/partidos", response_class=HTMLResponse)
def read_partidos(request: Request, session: Session = Depends(get_session)):
    """Muestra la lista de partidos."""
    try:
        partidos = session.exec(select(Partido)).all()
    except Exception as e:
        print(f"Error al cargar partidos: {e}")
        partidos = []

    context = {"request": request, "partidos": partidos}
    return templates.TemplateResponse("partidos.html", context)


@app.post("/partidos")
def create_partido(
        fecha_partido: str = Form(...),
        rival: str = Form(...),
        goles_sigmotoa: int = Form(...),
        goles_rival: int = Form(...),
        estado_str: str = Form(..., alias="estado"),
        session: Session = Depends(get_session)
):
    """Crea un nuevo partido, calcula el resultado implícito."""
    try:
        new_partido = Partido(
            fecha_partido=datetime.strptime(fecha_partido, "%Y-%m-%d").date(),
            rival=rival,
            goles_sigmotoa=goles_sigmotoa,
            goles_rival=goles_rival,
            estado=estado_str
        )

        session.add(new_partido)
        session.commit()
        session.refresh(new_partido)
        return RedirectResponse("/partidos", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el partido: {e}")