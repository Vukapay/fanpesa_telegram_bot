"""
Integration tests for the FastAPI metadata/health/readiness/liveness endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import _build_webhook_url, app
from app.webhooks.telegram import WEBHOOK_PATH


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


def test_webhook_aliases_return_503_when_not_configured(client: TestClient) -> None:
    for path in ("/webhook", "/telegram/webhook"):
        response = client.post(path, json={"update_id": 1})
        assert response.status_code == 503, path


def test_build_webhook_url_normalizes_common_values() -> None:
    assert _build_webhook_url("https://example.com") == f"https://example.com{WEBHOOK_PATH}"
    assert _build_webhook_url(f"https://example.com{WEBHOOK_PATH}") == f"https://example.com{WEBHOOK_PATH}"
    assert _build_webhook_url("https://example.com/telegram/webhook") == "https://example.com/telegram/webhook"
    assert _build_webhook_url("https://example.com/webhooks/telegram") == "https://example.com/webhooks/telegram"
