from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

#CREACIÓN DEL MODELO JUGADOR PARA LA BASE DE DATOS
class JugadorBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    numero_camiseta: int = Field(unique=True)
    fecha_nacimiento: datetime
    nacionalidad: str
    fotografia_url: Optional[str] = Field(default=None, description="URL de la FOTO del JUGADOR")
    pass
class Jugador(JugadorBase, table=True):
    #CARACTERÍSTICAS DEPORTIVAS DEL JUGADOR
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    pie_dominante: Optional[str] = None
    posicion: Optional[str] = None
    ano_ingreso_club: Optional[int] = None
    valor_mercado_col: Optional[float] = None
    estado_jugador: Optional[str] = None
    #RELACIONES CON OTROS MODELOS
    partidos: List["Partido"] = Relationship(back_populates="jugadores")
    estadisticas: List["Estadistica"] = Relationship(back_populates="jugador") #RELACIÓN CON EL MODELO ESTADISTICAS PARA SABER LAS ESTADISTICAS DE CADA JUGADOR
    pass


#CREACIÓN DEL MODELO ESTADISTICAS PARA DETERMINAR LAS ESTADISTICAS DE CADA JUGADOR
class Estadistica(SQLModel, table=True):
    #JUGADOR AL QUE PERTENECEN LAS ESTADISTICAS
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: Optional[int] = Field(default=None, foreign_key="jugadorbase.id")
    jugador: Optional[JugadorBase] = Relationship(back_populates="estadisticas")
    total_tiempo_jugado_min: Optional[int] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    faltas_cometidas: Optional[int] = None
    suspensiones: Optional[bool] = None
    pass

#CREACIÓN DEL MODELO PARTIDO
class Partido(SQLModel, table=True):
    #AGRUPACIÓN DE LAS ESTADISTICAS DE LOS JUGADORES EN CADA PARTIDO
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_partido: datetime
    jugadores: List[Jugador] = Relationship(back_populates="partidos")
    resultado: Optional[str] = None
    #SIGMOTOA SIEMPRE ES LOCAL
    goles_sigmotoa: Optional[int] = None
    pass

#ESQUEMAS PARA LA CREACIÓN DE JUGADORES Y LECTURA DE JUGADORES (PYDACTIC)
class JugadorRead(JugadorBase):
    id: int
    class Config:
        orm_mode = True
class JugadorCreate(JugadorBase):
    pass
class EstadisticaRead(SQLModel):
    id: int
    jugador_id: int
    total_tiempo_jugado_min: Optional[int]
    goles: Optional[int]
    asistencias: Optional[int]
    tarjetas_amarillas: Optional[int]
    tarjetas_rojas: Optional[int]
    faltas_cometidas: Optional[int]
    suspensiones: Optional[bool]
    class Config:
        orm_mode = True
class EstadisticaCreate(SQLModel):
    jugador_id: int
    total_tiempo_jugado_min: Optional[int]
    goles: Optional[int]
    asistencias: Optional[int]
    tarjetas_amarillas: Optional[int]
    tarjetas_rojas: Optional[int]
    faltas_cometidas: Optional[int]
    suspensiones: Optional[bool]
    pass
class PartidoRead(SQLModel):
    id: int
    fecha_partido: datetime
    resultado: Optional[str]
    goles_sigmotoa: Optional[int]
    class Config:
        orm_mode = True
class PartidoCreate(SQLModel):
    fecha_partido: datetime
    resultado: Optional[str]
    goles_sigmotoa: Optional[int]
    pass
#ESQUEMAS PARA LA CREACIÓN DE ESTADISTICAS Y LECTURA DE ESTADISTICAS (PYDACTIC)
class PartidoReadWithPlayers(PartidoRead):
    jugadores: List[JugadorRead] = []
    pass
class PartidoCreateWithPlayers(PartidoCreate):
    jugadores: List[int] = []
    pass
#ESQUEMAS PARA LA CREACIÓN DE ESTADISTICAS Y LECTURA DE ESTADISTICAS (PYDACTIC)
class EstadisticaReadWithPlayer(EstadisticaRead):
    jugador: Optional[JugadorRead]
    pass
class EstadisticaCreateWithPlayer(EstadisticaCreate):
    pass


#ESQUEMAS PARA LA ACTUALIZACIÓN DE JUGADORES (PYDACTIC)
class JugadorUpdate(SQLModel):
    nombre: Optional[str] = None
    numero_camiseta: Optional[int] = None
    fecha_nacimiento: Optional[datetime] = None
    nacionalidad: Optional[str] = None
    fotografia_url: Optional[str] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    pie_dominante: Optional[str] = None
    posicion: Optional[str] = None
    ano_ingreso_club: Optional[int] = None
    valor_mercado_col: Optional[float] = None
    estado_jugador: Optional[str] = None
    pass
#ESQUEMAS PARA LA ACTUALIZACIÓN DE ESTADISTICAS (PYDACTIC)
class EstadisticaUpdate(SQLModel):
    total_tiempo_jugado_min: Optional[int] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    faltas_cometidas: Optional[int] = None
    suspensiones: Optional[bool] = None
    pass
#ESQUEMAS PARA LA ACTUALIZACIÓN DE PARTIDOS (PYDACTIC)
class PartidoUpdate(SQLModel):
    fecha_partido: Optional[datetime] = None
    resultado: Optional[str] = None
    goles_sigmotoa: Optional[int] = None
    pass