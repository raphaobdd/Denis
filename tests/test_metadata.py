import json
import os
import pandas as pd
import pytest
from datetime import date

# Caminho para o CSV de teste e JSON gerado
CSV_PATH = os.path.join(os.path.dirname(__file__), "../backend/asteroids_rows.csv")
JSON_PATH = os.path.join(os.path.dirname(__file__), "../backend/asteroids_metadata.json")

@pytest.fixture(scope="module", autouse=True)
def setup_csv_and_metadata():
    """Cria CSV de teste antes dos testes e gera o JSON de metadados."""
    # Cria CSV de teste
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["Ast1", "Ast2"],
        "diameter": [1.2, 3.4],
        "magnitude": [10, 12]
    })
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH, index=False)

    # Gera metadados em JSON
    linhas = len(df)
    colunas = len(df.columns)
    tamanho_MB = df.memory_usage(deep=True).sum() / 1024**2
    colunas_nomes = list(df.columns)

    metadados = {
        "nome_dataset": "asteroids_rows",
        "descricao": "Dados de asteroides de teste",
        "fonte": "Teste",
        "url_fonte": "",
        "licenca": "Public Domain",
        "data_extracao": date.today().isoformat(),
        "volume": {
            "linhas": linhas,
            "colunas": colunas,
            "tamanho_MB": round(tamanho_MB, 2),
            "colunas_nomes": colunas_nomes
        }
    }

    with open(JSON_PATH, "w") as f:
        json.dump(metadados, f, indent=4)

    yield  # roda os testes

    # Cleanup opcional
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    if os.path.exists(JSON_PATH):
        os.remove(JSON_PATH)


def test_csv_carregado():
    """Testa se o CSV foi carregado e contém colunas"""
    df = pd.read_csv(CSV_PATH)
    assert not df.empty
    assert len(df.columns) > 0


def test_metadados_gerados():
    """Testa se o JSON de metadados foi criado"""
    assert os.path.exists(JSON_PATH)
    with open(JSON_PATH) as f:
        metadados = json.load(f)

    # Verifica campos principais
    assert "nome_dataset" in metadados
    assert "volume" in metadados
    assert "linhas" in metadados["volume"]
    assert "colunas" in metadados["volume"]
    assert "tamanho_MB" in metadados["volume"]
    assert "colunas_nomes" in metadados["volume"]
    assert isinstance(metadados["volume"]["colunas_nomes"], list)
