"""
Telegram Application Factory

Builds the `python-telegram-bot` `Application`, registering commands
and menu-button handlers. Runs in polling mode for this milestone;
`app/webhooks/telegram.py` documents the future webhook-mode wiring.

Run with:

    python -m app.bot.application
"""

from __future__ import annotations

import re

from telegram import Update
from telegram.ext import (
    Application,
    BaseHandler,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.bot.commands.about import about
from app.bot.commands.help import help_command
from app.bot.commands.start import start
from app.bot.commands.support import build_support_text, support
from app.bot.handlers.deposit import build_deposit_text, deposit_handler
from app.bot.handlers.promotion import build_promotions_text, promotion_handler
from app.bot.handlers.wallet import build_wallet_text, wallet_handler
from app.bot.handlers.withdraw import build_withdraw_text, withdraw_handler
from app.bot.keyboards.inline import (
    launch_app_keyboard,
    promotions_keyboard,
    support_keyboard,
    wallet_keyboard,
)
from app.config.settings import settings
from app.core.constants import Buttons, CallbackData
from app.core.logger import get_logger

logger = get_logger(__name__)


def _button_filter(text: str) -> filters.BaseFilter:
    """Build a filter that matches an exact reply-keyboard button label."""
    return filters.Regex(rf"^{re.escape(text)}$")


async def _callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route inline-keyboard button taps (`callback_data`) to their content.

    Every inline button must be answered, otherwise Telegram leaves the
    button showing a loading spinner that quietly times out client-side —
    which is why the /start inline buttons looked like they "did nothing".
    """
    query = update.callback_query
    if query is None or query.message is None:
        return

    await query.answer()

    user = query.from_user
    logger.info(
        "action=callback data=%s user_id=%s username=%s", query.data, user.id, user.username
    )

    if query.data == CallbackData.WALLET:
        text = await build_wallet_text(user.id)
        await query.message.reply_text(
            text=text, parse_mode="Markdown", reply_markup=wallet_keyboard()
        )
    elif query.data == CallbackData.PROMOTIONS:
        text = await build_promotions_text()
        await query.message.reply_text(
            text=text, parse_mode="Markdown", reply_markup=promotions_keyboard()
        )
    elif query.data == CallbackData.DEPOSIT:
        text = await build_deposit_text(user.id)
        await query.message.reply_text(
            text=text, parse_mode="Markdown", reply_markup=wallet_keyboard()
        )
    elif query.data == CallbackData.WITHDRAW:
        text = await build_withdraw_text(user.id)
        await query.message.reply_text(
            text=text, parse_mode="Markdown", reply_markup=wallet_keyboard()
        )
    elif query.data == CallbackData.SUPPORT:
        await query.message.reply_text(
            build_support_text(), parse_mode="Markdown", reply_markup=support_keyboard()
        )
    elif query.data == CallbackData.OPEN_APP:
        await query.message.reply_text(
            text="👇 Tap below to launch FanPesa.",
            reply_markup=launch_app_keyboard(),
        )


def _build_handlers() -> list[BaseHandler]:
    """Return every command and menu-button handler for the bot."""
    return [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("about", about),
        CommandHandler("support", support),
        MessageHandler(_button_filter(Buttons.WALLET), wallet_handler),
        MessageHandler(_button_filter(Buttons.DEPOSIT), deposit_handler),
        MessageHandler(_button_filter(Buttons.WITHDRAW), withdraw_handler),
        MessageHandler(_button_filter(Buttons.PROMOTIONS), promotion_handler),
        MessageHandler(_button_filter(Buttons.ABOUT), about),
        MessageHandler(_button_filter(Buttons.SUPPORT), support),
        CallbackQueryHandler(_callback_query_handler),
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
