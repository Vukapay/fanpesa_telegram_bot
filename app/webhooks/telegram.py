"""
Telegram Webhook Endpoint

Only active in production, when `WEBHOOK_URL` is set. `app/main.py`
builds, starts, and registers the `python-telegram-bot` `Application`
on FastAPI startup (see its `lifespan`) and stores it on
`app.state.telegram_application`; this router just hands each
incoming update to that already-running application.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status
from telegram import Update

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/telegram")
async def telegram_webhook(request: Request) -> dict[str, bool]:
    """Receive a Telegram update and dispatch it to the running bot application."""
    application = request.app.state.telegram_application
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook mode is not configured — set WEBHOOK_URL and BOT_TOKEN.",
        )

    payload = await request.json()
    update = Update.de_json(payload, application.bot)
    await application.process_update(update)

    return {"ok": True}
