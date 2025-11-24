import pytest
from unittest.mock import patch
import sys
import os

# Adiciona raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mocka create_client antes de importar o app
with patch("backend.app.create_client") as mock_client:
    mock_client.return_value = None
    from backend.app import app, feature_names

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    data = rv.data.decode("utf-8")
    assert "Painel do Modelo de Asteroides" in data

def test_metrics(client):
    rv = client.get("/metrics")
    data = rv.data.decode("utf-8")
    assert rv.status_code == 200
    assert "Métricas" in data or "erro" in data

def test_test_model_page(client):
    rv = client.get("/test-model")
    data = rv.data.decode("utf-8")
    assert rv.status_code == 200
    assert "<form" in data

def test_predict_missing_model(client):
    app.model = None
    post_data = {feature_names[0]: 1.0} if feature_names else {"fake_feature": 1.0}
    rv = client.post("/predict", data=post_data)
    data = rv.data.decode("utf-8")
    assert rv.status_code in [400, 500]
    assert "Modelo ou preprocessadores não carregados" in data or "erro" in data
