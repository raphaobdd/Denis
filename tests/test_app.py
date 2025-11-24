import pytest
from unittest.mock import patch

# Primeiro patch do create_client, antes de importar app
with patch("backend.app.create_client") as mock_create:
    mock_create.return_value = None  # ou um mock se precisar
    from backend.app import app

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

def test_test_model_page(client):
    rv = client.get("/test-model")
    data = rv.data.decode("utf-8")
    assert rv.status_code == 200
    assert "<form" in data
