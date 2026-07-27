"""
Withdraw Handler

Responds to the "💸 Withdraw" menu button. Withdrawals are handled
inside the FanPesa Mini App; this handler shows the user's balance
and directs them there.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import wallet_keyboard
from app.core.constants import Buttons
from app.core.logger import get_logger
from app.platform.telegram import telegram_adapter

logger = get_logger(__name__)


async def build_withdraw_text(user_id: int) -> str:
    """Render the withdrawal prompt + current balance as a message body."""
    balance = await telegram_adapter.get_wallet_balance(user_id)

    return (
        "💸 *Withdraw from FanPesa*\n\n"
        f"Available balance: *{balance.balance:,.2f} {balance.currency}*\n\n"
        "Withdrawals are processed securely inside the FanPesa Mini App. "
        "Tap below to open it and request a withdrawal."
    )


async def withdraw_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current balance and direct the user to the Mini App to withdraw."""
    user = update.effective_user
    if user is None or update.message is None:
        return

    logger.info("action=withdraw user_id=%s username=%s", user.id, user.username)

    text = await build_withdraw_text(user.id)

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=wallet_keyboard(),
    )


WITHDRAW_BUTTON_TEXT = Buttons.WITHDRAW
