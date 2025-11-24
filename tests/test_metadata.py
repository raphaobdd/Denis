import json
import os
import pandas as pd
import pytest
from datetime import date

# Caminhos para o CSV de teste e JSON gerado
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "../backend/asteroids_rows.csv")
JSON_PATH = os.path.join(BASE_DIR, "../backend/asteroids_metadata.json")


@pytest.fixture(scope="module", autouse=True)
def setup_csv_and_metadata():
    """Cria CSV de teste e gera o JSON de metadados antes dos testes."""
    # Cria CSV de teste
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["Ast1", "Ast2"],
        "diameter": [1.2, 3.4],
        "magnitude": [10, 12]
    })
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH, index=False)

    # Gera JSON de metadados
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

    yield  # executa os testes

    # Cleanup
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    if os.path.exists(JSON_PATH):
        os.remove(JSON_PATH)


def test_csv_carregado():
    """Verifica se o CSV foi carregado corretamente."""
    df = pd.read_csv(CSV_PATH)
    assert not df.empty
    assert len(df.columns) > 0


def test_metadados_gerados():
    """Verifica se JSON de metadados foi criado e contém campos corretos."""
    assert os.path.exists(JSON_PATH)
    with open(JSON_PATH) as f:
        metadados = json.load(f)

    # Checagem de campos principais
    assert "nome_dataset" in metadados
    assert "volume" in metadados
    assert "linhas" in metadados["volume"]
    assert "colunas" in metadados["volume"]
    assert "tamanho_MB" in metadados["volume"]
    assert "colunas_nomes" in metadados["volume"]
    assert isinstance(metadados["volume"]["colunas_nomes"], list)
