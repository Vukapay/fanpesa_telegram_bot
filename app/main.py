"""
FastAPI Application Entry Point

Exposes application metadata and health/readiness/liveness endpoints.
The Telegram bot itself runs separately in polling mode via
`python -m app.bot.application`; this process is the future home of
webhook-mode Telegram updates and any REST endpoints FanPesa needs.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.mock import mock_api
from app.config.settings import settings
from app.core.logger import logger
from app.webhooks.telegram import router as telegram_webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info(
        "FanPesa application starting (env=%s, version=%s)",
        settings.environment,
        settings.app_version,
    )

    yield

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
async def health() -> dict:
    """Health check backed by the mock FanPesa API until the real backend is available."""
    return await mock_api.heartbeat()


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check — is the app ready to accept traffic?"""
    return {"status": "ready"}


@app.get("/live")
async def live() -> dict[str, str]:
    """Liveness check — is the process still running?"""
    return {"status": "alive"}
