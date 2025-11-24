import json
import os
import pandas as pd
import pytest

# Importa o script de geração de metadados
import importlib.util

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "generate_metadata.py")  # ajuste se necessário
spec = importlib.util.spec_from_file_location("generate_metadata", SCRIPT_PATH)
metadata_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata_module)

def test_csv_carregado():
    """Testa se o CSV foi carregado e contém colunas"""
    df = pd.read_csv("asteroids_rows.csv")
    assert not df.empty
    assert len(df.columns) > 0

def test_metadados_gerados():
    """Testa se o JSON de metadados foi criado"""
    assert os.path.exists("asteroids_metadata.json")
    with open("asteroids_metadata.json") as f:
        metadados = json.load(f)
    
    # Verifica campos principais
    assert "nome_dataset" in metadados
    assert "volume" in metadados
    assert "linhas" in metadados["volume"]
    assert "colunas" in metadados["volume"]
    assert "tamanho_MB" in metadados["volume"]
    assert "colunas_nomes" in metadados["volume"]
    assert isinstance(metadados["volume"]["colunas_nomes"], list)
