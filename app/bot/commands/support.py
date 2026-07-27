"""
/support command.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import support_keyboard
from app.core.constants import SUPPORT_EMAIL
from app.core.logger import get_logger

logger = get_logger(__name__)


def build_support_text() -> str:
    """Render the support contact message body."""
    return f"""
🛟 *Need help?*

Our support team is here for you.

📧 Email: {SUPPORT_EMAIL}
🌐 Website: https://www.fanpesa.com
"""


async def support(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=support user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    await update.message.reply_text(
        build_support_text(),
        parse_mode="Markdown",
        reply_markup=support_keyboard(),
    )
