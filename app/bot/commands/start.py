"""
/start command.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import launch_app_keyboard
from app.bot.keyboards.main_menu import main_menu
from app.core.logger import get_logger

logger = get_logger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=start user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    await update.message.reply_text(
        text="""
🎉 *Welcome to FanPesa!*

The fastest betting experience inside Telegram.

✅ Deposit
✅ Bet
✅ Win
✅ Withdraw

👇 Tap below to launch FanPesa.
""",
        parse_mode="Markdown",
        reply_markup=launch_app_keyboard(),
    )

    await update.message.reply_text(
        text="Use the menu below any time to jump straight to a feature.",
        reply_markup=main_menu(),
    )
