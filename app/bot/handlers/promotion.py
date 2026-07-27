"""
Promotion Handler

Responds to the "🎁 Promotions" menu button by listing currently
active FanPesa promotions.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import promotions_keyboard
from app.core.constants import Buttons
from app.core.logger import get_logger
from app.platform.telegram import telegram_adapter

logger = get_logger(__name__)


async def build_promotions_text() -> str:
    """Render the active-promotions list as a message body."""
    promotions = await telegram_adapter.list_promotions()

    if not promotions:
        return "🎁 There are no active promotions right now — check back soon!"

    lines = ["🎁 *Active Promotions*", ""]
    for promo in promotions:
        lines.append(f"*{promo.title}*\n{promo.description}\n")
    return "\n".join(lines)


async def promotion_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List currently active promotions."""
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=promotions user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    text = await build_promotions_text()

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=promotions_keyboard(),
    )


PROMOTIONS_BUTTON_TEXT = Buttons.PROMOTIONS
