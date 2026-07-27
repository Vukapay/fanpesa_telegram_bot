"""
/about command.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.core.constants import COMPANY_NAME, WEBSITE
from app.core.logger import get_logger

logger = get_logger(__name__)


async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=about user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    await update.message.reply_text(
        f"""
ℹ️ *{COMPANY_NAME}*

Fast. Secure. Reliable.

FanPesa brings a full betting experience straight into Telegram,
backed by the same platform available at {WEBSITE}.

🌐 Website: {WEBSITE}
""",
        parse_mode="Markdown",
    )
