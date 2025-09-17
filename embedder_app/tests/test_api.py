from fastapi.testclient import TestClient
import pytest
from app.app import WebApp


@pytest.fixture
def client():
    app = WebApp()
    return TestClient(app)


def test_ping(client):
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_revert_vector_success(client):
    payload = [1.0, 2.0, 3.0]
    response = client.post("/api/v1/revert_vector", json=payload)
    assert response.status_code == 200
    assert response.json() == [3.0, 2.0, 1.0]


def test_revert_vector_invalid_type(client):
    payload = {"vector": "not_a_list"}
    response = client.post("/api/v1/revert_vector", json=payload)
    assert response.status_code == 422


def test_revert_vector_missing_field(client):
    payload = {}
    response = client.post("/api/v1/revert_vector", json=payload)
    assert response.status_code == 422


def test_unknown_route(client):
    response = client.get("/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
