"""
Referral Handler

Responds to the "👥 Invite Friends" action by sharing the user's
referral link and stats. Not currently bound to a persistent menu
button, but available for the /support or inline "Invite" callback.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.core.constants import BOT_USERNAME
from app.core.logger import get_logger
from app.platform.telegram import telegram_adapter

logger = get_logger(__name__)


async def referral_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's referral link and stats."""
    user = update.effective_user
    if user is None or update.message is None:
        return

    logger.info("action=referral user_id=%s username=%s", user.id, user.username)

    referral_code = await telegram_adapter.get_referral_code(user.id)
    stats = await telegram_adapter.get_referral_stats(user.id)
    invite_link = f"https://t.me/{BOT_USERNAME}?start=ref_{referral_code}"

    await update.message.reply_text(
        text=(
            "👥 *Invite Friends to FanPesa*\n\n"
            f"Your invite link:\n{invite_link}\n\n"
            f"Total referrals: *{stats['total_referrals']}*\n"
            f"Total earned: *{stats['total_earned']:,.2f} KES*"
        ),
        parse_mode="Markdown",
    )
