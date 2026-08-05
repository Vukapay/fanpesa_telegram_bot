"""
FastAPI Application Entry Point

Exposes application metadata and health/readiness/liveness endpoints.

In local development (`WEBHOOK_URL` unset), the Telegram bot runs as
its own separate polling process via `python -m app.bot.application`
and this process only serves health checks — nothing here touches
Telegram's API.

In production (`WEBHOOK_URL` set — e.g. behind Cloudflare), this
process *is* the bot: on startup it builds and starts the
`python-telegram-bot` `Application` once, registers it as Telegram's
webhook target, and serves updates via `app/webhooks/telegram.py`.
The polling process must not also be running at the same time as
webhook mode — Telegram only delivers updates one way at a time.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI

from app.bot.application import create_application
from app.config.settings import settings
from app.core.logger import logger
from app.webhooks.telegram import WEBHOOK_PATH
from app.webhooks.telegram import router as telegram_webhook_router


def _is_bot_token_configured() -> bool:
    return bool(settings.bot_token) and settings.bot_token != "CHANGE_ME"


def _build_webhook_url(base_url: str) -> str:
    """Normalize the configured base URL into a Telegram-compatible webhook target."""
    normalized = base_url.rstrip("/")
    for suffix in (WEBHOOK_PATH, "/webhook", "/telegram/webhook"):
        if normalized.endswith(suffix):
            return normalized
    return f"{normalized}{WEBHOOK_PATH}"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        "FanPesa application starting (env=%s, version=%s)",
        settings.environment,
        settings.app_version,
    )

    app.state.telegram_application = None

    if settings.webhook_url and _is_bot_token_configured():
        application = create_application()
        await application.initialize()
        await application.start()

        webhook_url = _build_webhook_url(settings.webhook_url)
        try:
            await application.bot.set_webhook(url=webhook_url)
        except Exception as exc:  # pragma: no cover - defensive logging for deployment issues
            logger.warning("Telegram webhook registration failed for %s: %s", webhook_url, exc)

        app.state.telegram_application = application
        logger.info("Telegram webhook target configured at %s", webhook_url)
    elif settings.webhook_url:
        logger.warning(
            "WEBHOOK_URL is set but BOT_TOKEN is not configured — skipping webhook setup"
        )
    else:
        logger.info("WEBHOOK_URL not set — Telegram bot must be run separately via polling")

    yield

    application = app.state.telegram_application
    if application is not None:
        await application.bot.delete_webhook()
        await application.stop()
        await application.shutdown()

    logger.info("FanPesa application stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(telegram_webhook_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Application metadata."""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check — confirms the process is up and able to serve requests."""
    return {"status": "ok", "time": datetime.now(UTC).isoformat()}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check — is the app ready to accept traffic?"""
    return {"status": "ready"}


@app.get("/live")
async def live() -> dict[str, str]:
    """Liveness check — is the process still running?"""
    return {"status": "alive"}
