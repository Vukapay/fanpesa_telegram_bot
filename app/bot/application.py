"""
Telegram Application Factory

Builds the `python-telegram-bot` `Application`, registering commands
and menu-button handlers. Runs in polling mode for this milestone;
`app/webhooks/telegram.py` documents the future webhook-mode wiring.

Open FanPesa, Register, Login, Deposit, Withdraw, and Promotion are
all `web_app` buttons (see `app/bot/keyboards/`) — Telegram opens the
Mini App for these entirely client-side, so no handler is registered
for them here. `/about` remains available as a slash command even
though it's no longer on the persistent menu.

Run with:

    python -m app.bot.application
"""

from __future__ import annotations

import re

from telegram.ext import (
    Application,
    BaseHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from app.bot.commands.about import about
from app.bot.commands.help import help_command
from app.bot.commands.start import start, aviator_promo
from app.bot.commands.support import support
from app.config.settings import settings
from app.core.constants import Buttons
from app.core.logger import get_logger

logger = get_logger(__name__)


def _button_filter(text: str) -> filters.BaseFilter:
    """Build a filter that matches an exact reply-keyboard button label."""
    return filters.Regex(rf"^{re.escape(text)}$")


def _build_handlers() -> list[BaseHandler]:
    """Return every command and menu-button handler for the bot."""
    return [
        CommandHandler("start", start),
        CallbackQueryHandler(aviator_promo, pattern=r"^aviator_promo$"),
        CommandHandler("help", help_command),
        CommandHandler("about", about),
        CommandHandler("support", support),
        MessageHandler(_button_filter(Buttons.SUPPORT), support),
    ]


def create_application() -> Application:
    """Build and configure the Telegram `Application` for FanPesa."""
    application = Application.builder().token(settings.bot_token).build()

    for handler in _build_handlers():
        application.add_handler(handler)

    logger.info("Telegram application configured with %d handlers", len(_build_handlers()))

    return application


def main() -> None:
    """Entry point for `python -m app.bot.application` (polling mode)."""
    application = create_application()
    logger.info("Starting FanPesa Telegram bot in polling mode")
    application.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
