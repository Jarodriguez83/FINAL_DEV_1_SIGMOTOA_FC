# SIGMOTOA FC - Sistema de Gestión de Desempeño de Jugadores 

SIGMOTOA FC es un sistema web diseñado para gestionar y analizar el desempeño de los jugadores del equipo partido a partido. Este sistema tiene como objetivo resolver la pérdida de registros históricos y mejorar la planificación estratégica del equipo.

## Características

- **Registro de jugadores**: Permite almacenar información detallada de cada jugador del plantel.
  ### DATOS PERSONALES:
  - Nombre Completo.
  - N° de Camiseta(Este va a hacer como el ID, o sea va a ser unico).
  - Fecha Nacimiento (Para tener la edad actualizada)
  - Fotografia (Esencial pero opcional)
  - Nacionalidad (Se va a tener algunas restricciones en algunas ligas)

  ### CARACTERISTICAS DEPORTIVAS:
  -Altura (cm)
  - Peso (km)
  - Pie Dominante
  - Posicion (Defensa, Central, Lateral, Mediocampo, Centro, Punta)
  - Valor de Mercado $$$
  - Jugador Activo (Si tiene relacion laboral con algun club) 

- **Seguimiento de desempeño**: Registra estadísticas y el rendimiento de los jugadores en cada partido
- **Análisis estratégico**: Facilita la consulta de datos para la planificación de estrategias del equipo.
- **Gestión de estados**: Controla el estado de los jugadores, como activo(Si el Jugador esta en relacion laboral con un club ), lesionado, suspendido (Jugador con tarjeta).


## Tecnologías utilizadas

- **Backend:** FastAPI para la creación de APIs rápidas y eficientes.
- **Base de datos:** SQLite con SQLModel para la gestión de datos.
- **Lenguaje:** Python.
- **Servidor:** Uvicorn para el despliegue del servidor ASGI.

## Instalación y configuración

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
  

2. Crea y vincula un entorno virtual:

   Dato: Estoy si estas usando Visual Studio Code, si usas PyCharm la activacion es automatica.

python -m venv .venv  
source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
 ## Modelos de Datos

El sistema utiliza **SQLModel** para definir los modelos de datos y gestionar la base de datos. 

## Modelos
### Jugador
El modelo `Jugador` representa a los jugadores del equipo. Incluye información básica y características deportivas:

- **Campos principales**:
  - `id`: Identificador único del jugador.
  - `nombre`: Nombre del jugador.
  - `numero_camiseta`: Número de camiseta (único).
  - `fecha_nacimiento`: Fecha de nacimiento.
  - `nacionalidad`: Nacionalidad.
  - `fotografia_url`: URL de la fotografía del jugador.
  - `altura_cm`: Altura en centímetros.
  - `peso_kg`: Peso en kilogramos.
  - `pie_dominante`: Pie dominante del jugador.
  - `posicion`: Posición en el campo.
  - `ano_ingreso_club`: Año de ingreso al club.
  - `valor_mercado_col`: Valor de mercado en pesos colombianos.
  - `estado_jugador`: Estado actual del jugador (e.g., ACTIVO, INACTIVO).

### Estadistica
El modelo `Estadistica` almacena las estadísticas de cada jugador en los partidos:

- **Campos principales**:
  - `id`: Identificador único de la estadística.
  - `jugador_id`: Relación con el jugador al que pertenece la estadística.
  - `total_tiempo_jugado_min`: Minutos jugados en total.
  - `goles`: Goles anotados.
  - `asistencias`: Asistencias realizadas.
  - `tarjetas_amarillas`: Número de tarjetas amarillas.
  - `tarjetas_rojas`: Número de tarjetas rojas.
  - `faltas_cometidas`: Faltas cometidas.
  - `suspensiones`: Si el jugador está suspendido.

### Partido
El modelo `Partido` agrupa las estadísticas de los jugadores en cada partido:

- **Campos principales**:
  - `id`: Identificador único del partido.
  - `fecha_partido`: Fecha del partido.
  - `resultado`: Resultado del partido.
  - `goles_sigmotoa`: Goles anotados por el equipo SIGMOTOA FC.


4.Ejecuta el servidor 
uvicorn main:app --reload

## **Autores**

_**Este proyecto fue desarrollado por:**_

 ```bash
- Jader Santiago Nieves Tami - Código: 67001539
- Jhon Alexander Rodríguez Redondo - Código: 67001483 
