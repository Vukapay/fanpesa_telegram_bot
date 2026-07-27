"""
Telegram Webhook Endpoint

The bot runs in polling mode for this milestone (see
`app/bot/application.py`, run via `python -m app.bot.application`).
This router documents and implements the webhook-mode wiring for
when FanPesa moves off polling in production: Telegram would be
configured (via `setWebhook`) to POST updates to
`{WEBHOOK_URL}/webhooks/telegram`.
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import Application

from app.bot.application import create_application
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

_application: Application | None = None


async def _get_application() -> Application:
    """Lazily build and initialize the Telegram application, once."""
    global _application

    if _application is None:
        _application = create_application()
        await _application.initialize()

    return _application


@router.post("/telegram")
async def telegram_webhook(request: Request) -> dict[str, bool]:
    """Receive a Telegram update and dispatch it to the bot application."""
    payload = await request.json()
    application = await _get_application()

    update = Update.de_json(payload, application.bot)
    await application.process_update(update)

    return {"ok": True}
