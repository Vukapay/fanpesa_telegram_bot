"""
/help command.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.core.logger import get_logger

logger = get_logger(__name__)


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    user = update.effective_user
    logger.info(
        "action=help user_id=%s username=%s",
        user.id if user else None,
        user.username if user else None,
    )

    await update.message.reply_text("""
Available Commands

/start — show the welcome message and launch FanPesa
/help — show this message
/about — learn more about FanPesa
/support — message our support team directly on Telegram

✈️ Aviator, 📝 Register, 🔐 Login, 💳 Deposit, 💸 Withdraw, and
🎁 Promotion open the FanPesa Mini App directly from the menu below —
everything happens without ever leaving Telegram.

Betting itself happens inside the FanPesa Mini App — tap
"🚀 Open FanPesa" to place bets, track odds, and manage your slips,
or jump straight into "✈️ Aviator", our most popular game.
""")
