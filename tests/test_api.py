import os
import sys
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Ensure project path is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from app.main import app, df

client = TestClient(app)

def test_dataset_record_count():
    # Verify that the Excel file has exactly 100 rows
    assert len(df) == 100, f"Expected 100 records, found {len(df)}"

def test_variables_count():
    # Expect exactly 9 columns (variables) in the dataframe
    expected = 9
    actual = len(df.columns)
    assert actual == expected, f"Expected {expected} variables, found {actual}: {df.columns.tolist()}"

def test_get_all_records():
    response = client.get("/datos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100

def test_get_record_by_id():
    # Choose a known id (assuming 0-indexed after loading)
    record_id = 0  # use the first index as record ID
    response = client.get(f"/datos/{record_id}")
    assert response.status_code == 200
    record = response.json()
    assert record["id"] == record_id

def test_statistics_endpoint():
    response = client.get("/estadisticas")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_registros"] == 100
    # distribution should be a list of dicts with 'nivel_de_dominio' and 'cantidad'
    assert isinstance(stats["distribucion_nivel_dominio"], list)

