"""
Integration tests for the FastAPI metadata/health/readiness/liveness endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    # Runs the real lifespan (startup/shutdown) — with no WEBHOOK_URL
    # configured in tests, this must skip Telegram entirely and never
    # make a network call.
    with TestClient(app) as test_client:
        yield test_client


def test_root_returns_application_metadata(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["application"]
    assert body["version"]
    assert body["environment"]


def test_health_returns_ok_status(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_returns_ready(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_live_returns_alive(client: TestClient) -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_webhook_returns_503_when_not_configured(client: TestClient) -> None:
    response = client.post("/webhooks/telegram", json={"update_id": 1})

    assert response.status_code == 503
