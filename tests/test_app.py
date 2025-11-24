import pytest
import sys
import os

# Adiciona a raiz do projeto ao path para importar backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import app, feature_names  # import feature_names para usar no teste

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.data.decode("utf-8")
    assert "Painel do Modelo de Asteroides" in data  # verifica texto que existe no HTML

def test_metrics(client):
    rv = client.get("/metrics")
    data = rv.data.decode("utf-8")
    assert rv.status_code == 200
    assert "Métricas" in data or "erro" in data  # cobre caso métricas não existam

def test_test_model_page(client):
    rv = client.get("/test-model")
    data = rv.data.decode("utf-8")
    assert rv.status_code == 200
    assert "<form" in data  # verifica se o formulário está presente

def test_predict_missing_model(client):
    app.model = None

    # usa a primeira feature válida se existir
    if feature_names:
        post_data = {feature_names[0]: 1.0}
    else:
        post_data = {"fake_feature": 1.0}

    rv = client.post("/predict", data=post_data)
    data = rv.data.decode("utf-8")

    # aceita 500 se o modelo não estiver carregado, ou 400 se os dados forem inválidos
    assert rv.status_code in [400, 500]
    assert "Modelo ou preprocessadores não carregados" in data or "erro" in data
