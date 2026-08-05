"""Unit tests for application settings normalization."""

from app.config.settings import Settings


def test_webhook_url_strips_misconfigured_env_prefix() -> None:
    settings = Settings(webhook_url="WEBHOOK_URL=https://example.com/webhook")

    assert settings.webhook_url == "https://example.com/webhook"


def test_webhook_url_keeps_normal_value() -> None:
    settings = Settings(webhook_url="https://example.com/webhooks/telegram")

    assert settings.webhook_url == "https://example.com/webhooks/telegram"
