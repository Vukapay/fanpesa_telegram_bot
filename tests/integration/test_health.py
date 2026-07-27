"""
Integration tests for the FastAPI metadata/health/readiness/liveness endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_application_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["application"]
    assert body["version"]
    assert body["environment"]


def test_health_returns_ok_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_returns_ready() -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_live_returns_alive() -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
