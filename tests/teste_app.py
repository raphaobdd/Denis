import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Testa se a rota '/' retorna 200."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"index" in rv.data  # garante que a página contém a palavra "index"

def test_metrics(client):
    """Testa a rota '/metrics'."""
    rv = client.get("/metrics")
    data = rv.data.decode("utf-8")  # converte bytes para string
    assert rv.status_code == 200
    assert "Métricas" in data or "erro" in data


def test_test_model_page(client):
    """Testa se a rota '/test-model' retorna a página de teste."""
    rv = client.get("/test-model")
    assert rv.status_code == 200
    assert b"<form" in rv.data  # verifica se contém formulário

def test_predict_missing_model(client):
    """Testa predição quando o modelo não está carregado."""
    app.model = None
    rv = client.post("/predict", data={"fake_feature": 1})
    data = rv.data.decode("utf-8")  # converte bytes para string
    assert rv.status_code == 500
    assert "Modelo ou preprocessadores não carregados" in data

