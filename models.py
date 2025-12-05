
from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


# --- ENUMS ---
class EstadoJugadorEnum(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    LESIONADO = "LESIONADO"
    SUSPENDIDO = "SUSPENDIDO"
    AMONESTADO = "AMONESTADO"


class PartidoEstadoEnum(str, Enum):
    PROGRAMADO = "PROGRAMADO"
    FINALIZADO = "FINALIZADO"


class PosicionEnum(str, Enum):
    POR = "PORTERO"
    DEF = "DEFENSA"
    MED = "MEDIOCAMPISTA"
    DEL = "DELANTERO"


class PieDominanteEnum(str, Enum):
    DERECHO = "DERECHO"
    IZQUIERDO = "IZQUIERDO"
    AMBOS = "AMBOS"


# --- 1. MODELO JUGADOR ---
class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    numero_camiseta: int = Field(unique=True, index=True, gt=0)  # Debe ser > 0
    fecha_nacimiento: date
    nacionalidad: str = Field(max_length=50)
    fotografia_url: Optional[str] = None
    altura_cm: int = Field(gt=100)
    peso_kg: int = Field(gt=30)

    # Campos con Enums
    pie_dominante: PieDominanteEnum
    posicion: PosicionEnum

    # Restricciones de fecha
    ano_ingreso_club: int = Field(ge=1900, le=datetime.now().year)
    valor_mercado_col: int = Field(ge=0)
    estado_jugador: EstadoJugadorEnum = Field(default=EstadoJugadorEnum.ACTIVO)

    sancion: Optional[str] = Field(default=None, description="Descripción si hay sanción activa")

    # Relación uno a muchos con estadísticas
    estadisticas: List["EstadisticaJugador"] = Relationship(back_populates="jugador")


# --- 2. MODELO PARTIDO ---
class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_partido: date = Field(index=True)
    rival: str = Field(max_length=100)

    # Campos de resultado (la lógica se aplica en la propiedad)
    goles_sigmotoa: Optional[int] = Field(default=0, ge=0)
    goles_rival: Optional[int] = Field(default=0, ge=0)

    estado: PartidoEstadoEnum = Field(default=PartidoEstadoEnum.PROGRAMADO)

    # Relación uno a muchos con estadísticas de jugadores
    estadisticas: List["EstadisticaJugador"] = Relationship(back_populates="partido")

    @property
    def resultado_simple(self) -> str:
        """
        Determina si el partido fue GANADO, EMPATADO o PERDIDO para Sigamotoa FC
        (siempre es local).
        """
        if self.goles_sigmotoa is None or self.goles_rival is None:
            return "N/A"

        if self.goles_sigmotoa > self.goles_rival:
            return "GANADO"
        elif self.goles_sigmotoa == self.goles_rival:
            return "EMPATADO"
        else:
            return "PERDIDO"


# --- 3. MODELO ESTADÍSTICA POR PARTIDO ---
class EstadisticaJugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Claves foráneas (Relación Muchos a Muchos)
    jugador_id: int = Field(foreign_key="jugador.id", index=True)
    partido_id: int = Field(foreign_key="partido.id", index=True)

    # Métricas del partido
    goles: int = Field(default=0, ge=0)
    asistencias: int = Field(default=0, ge=0)
    tarjeta_amarilla: int = Field(default=0, ge=0, le=2)
    tarjeta_roja: int = Field(default=0, ge=0, le=1)
    minutos_jugados: int = Field(default=0, ge=0, le=120)
    lesionado: bool = Field(default=False)
    observaciones: Optional[str] = None

    # Relaciones de vuelta
    jugador: Optional[Jugador] = Relationship(back_populates="estadisticas")
    partido: Optional[Partido] = Relationship(back_populates="estadisticas")

    @property
    def sancion(self) -> Optional[str]:
        """Devuelve descripción de sanción si aplica."""
        if self.tarjeta_roja:
            return "SANCIONADO (Tarjeta Roja)"
        elif self.tarjeta_amarilla >= 2:
            return "SANCIONADO (Doble Amarilla)"
        return None

    @property
    def estado_participacion(self) -> str:
        """Determina el estado del jugador en ese partido específico."""
        if self.lesionado:
            return "LESIONADO"
        elif self.sancion:
            return "SANCIONADO"
        elif self.tarjeta_amarilla > 0:
            return "AMONESTADO"
        return "NORMAL"