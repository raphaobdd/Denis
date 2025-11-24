import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mocka create_client antes de importar o app
with patch("backend.app.create_client"):
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
    assert rv.status_code == 200
    data = rv.data.decode("utf-8")
    assert "<form" in data
