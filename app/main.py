import os
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load dataset
DATA_FILE = Path(__file__).parent.parent / "nexdrive_100_datos.xlsx"
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset file not found at {DATA_FILE}")

df = pd.read_excel(DATA_FILE, engine="openpyxl")
# Ensure there is an 'id' column; if not, create one based on the index
# No extra 'id' column is added; keep original columns as‑is
# We'll use the DataFrame index as the record identifier.
# The DataFrame itself remains unchanged.



# Convert DataFrame to list of dicts for fast lookup
records = df.to_dict(orient="records")

app = FastAPI(title="NexDrive Academic API", version="0.1.0")

# CORS configuration – can be overridden via env var (comma‑separated list)
origins_env = os.getenv("ALLOWED_ORIGINS", "*")
if origins_env.strip() == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [origin.strip() for origin in origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Record(BaseModel):
    """Pydantic model representing a single dataset row."""

    # Dynamically accept any fields from the dataset
    class Config:
        orm_mode = True
        extra = "allow"

@app.get("/datos", response_model=List[Record])
def get_all(
    tema: Optional[str] = Query(None, description="Filtrar por tema"),
    dificultad: Optional[str] = Query(None, description="Filtrar por dificultad"),
    nivel_dominio: Optional[str] = Query(None, description="Filtrar por nivel de dominio"),
):
    """Devuelve los 100 registros (o un subconjunto filtrado) añadiendo un campo `id` basado en el índice del DataFrame."""
    filtered = df
    if tema is not None:
        filtered = filtered[filtered["tema"].astype(str).str.contains(tema, case=False, na=False)]
    if dificultad is not None:
        filtered = filtered[filtered["dificultad"].astype(str).str.contains(dificultad, case=False, na=False)]
    if nivel_dominio is not None:
        filtered = filtered[filtered["nivel de dominio"].astype(str).str.contains(nivel_dominio, case=False, na=False)]
    # Convert to list of dicts and inject id from the DataFrame index
    records = filtered.reset_index().to_dict(orient="records")
    for rec in records:
        rec["id"] = rec.pop("index")  # rename temporary index column to id
    return records

def get_by_id(record_id: int):
    """Obtiene un registro específico por su ID (índice 0‑based)."""
    if record_id < 0 or record_id >= len(df):
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    # Get the row, add an 'id' field based on the index
    row = df.iloc[record_id].to_dict()
    row["id"] = record_id
    return row

@app.get("/estadisticas")
def statistics():
    """Muestra estadísticas básicas del dataset."""
    total = len(df)
    # Suponemos que la columna se llama exactamente "nivel de dominio"
    if "nivel de dominio" in df.columns:
        distribution = (
            df["nivel de dominio"]
            .value_counts()
            .rename_axis("nivel_de_dominio")
            .reset_index(name="cantidad")
            .to_dict(orient="records")
        )
    else:
        distribution = []
    return {"total_registros": total, "distribucion_nivel_dominio": distribution}

