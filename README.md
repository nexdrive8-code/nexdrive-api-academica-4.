# NexDrive Academic API

## Descripción

API REST académica construida con **FastAPI** que permite consultar los 100 registros del dataset de inteligencia artificial de NexDrive. Provee los siguientes endpoints:

- `GET /datos` – devuelve todos los registros (con soporte de filtros por `tema`, `dificultad` y `nivel_dominio`).
- `GET /datos/{id}` – devuelve un registro concreto por su identificador.
- `GET /estadisticas` – estadísticas básicas del dataset (total de registros y distribución por nivel de dominio).

La documentación interactiva está disponible en `http://localhost:8000/docs`.

## Requisitos

- Python 3.9 o superior
- `pip`

## Instalación

```bash
# Clonar o copiar el proyecto en tu máquina
cd path/to/nexdrive-api-academica

# (Opcional) crear un entorno virtual
python -m venv venv
source venv/Scripts/activate   # Windows
# o
# source venv/bin/activate   # Unix

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Esto iniciará el servidor en `http://localhost:8000`. Visita `http://localhost:8000/docs` para explorar la documentación Swagger.

## Pruebas

El proyecto incluye pruebas con **pytest**. Para ejecutarlas:

```bash
pytest
```

Todas las pruebas deben pasar y confirmar que la API devuelve exactamente 100 registros.

## Notas

- El archivo de datos `NexDrive_100_datos.xlsx` debe estar en la raíz del proyecto (ya está incluido).
- La configuración CORS se puede ajustar mediante la variable de entorno `ALLOWED_ORIGINS` (valor por defecto `*`).

---

*Este proyecto es únicamente con fines académicos y no está conectado al repositorio original de NexDrive.*
