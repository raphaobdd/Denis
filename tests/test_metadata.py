import sys
import os
import json
import pandas as pd
import pytest
import importlib.util

# Adiciona a pasta backend ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

# Caminho para o script de geração de metadados
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "../backend/generate_metadata.py")

# Importa dinamicamente o módulo
spec = importlib.util.spec_from_file_location("generate_metadata", SCRIPT_PATH)
metadata_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata_module)


def test_csv_carregado():
    """Testa se o CSV foi carregado e contém colunas"""
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../backend/asteroids_rows.csv"))
    assert not df.empty
    assert len(df.columns) > 0


def test_metadados_gerados(tmp_path):
    """Testa se o JSON de metadados é criado corretamente"""
    output_file = tmp_path / "asteroids_metadata.json"

    # Chama a função de geração de metadados, ajustando para gerar no tmp_path
    metadata_module.generate_metadata(output_file=str(output_file))

    # Verifica se o arquivo foi criado
    assert output_file.exists()

    # Carrega o JSON e valida campos principais
    with open(output_file) as f:
        metadados = json.load(f)

    assert "nome_dataset" in metadados
    assert "volume" in metadados
    volume = metadados["volume"]
    assert "linhas" in volume
    assert "colunas" in volume
    assert "tamanho_MB" in volume
    assert "colunas_nomes" in volume
    assert isinstance(volume["colunas_nomes"], list)
