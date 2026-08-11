"""
Telegram Webhook Endpoint

Only active in production, when `WEBHOOK_URL` is set. `app/main.py`
builds, starts, and registers the `python-telegram-bot` `Application`
on FastAPI startup (see its `lifespan`) and stores it on
`app.state.telegram_application`; this router just hands each
incoming update to that already-running application.
"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from telegram import Update

router = APIRouter(tags=["webhooks"])
WEBHOOK_PATH = "/webhooks/telegram"


@router.post(WEBHOOK_PATH)
@router.post("/webhook")
@router.post("/telegram/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks) -> dict[str, bool]:
    """Receive a Telegram update and dispatch it to the running bot application.

    Acknowledges Telegram immediately and processes the update in the
    background. Awaiting the full handler chain here (which includes
    outbound Telegram API calls, e.g. `reply_text`/`answer`) delays the
    response enough to trigger Telegram's webhook retries (duplicate
    commands) and to let queued callback queries go stale before
    `answer()` is called on them.
    """
    application = request.app.state.telegram_application
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook mode is not configured — set WEBHOOK_URL and BOT_TOKEN.",
        )

    payload = await request.json()
    update = Update.de_json(payload, application.bot)
    background_tasks.add_task(application.process_update, update)

    return {"ok": True}
