"""
Deposit Handler

Responds to the "💳 Deposit" menu button. Deposits are handled
inside the FanPesa Mini App (where real payment methods live); this
handler shows the user's balance and directs them there.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import wallet_keyboard
from app.core.constants import Buttons
from app.core.logger import get_logger
from app.platform.telegram import telegram_adapter

logger = get_logger(__name__)


async def build_deposit_text(user_id: int) -> str:
    """Render the deposit prompt + current balance as a message body."""
    balance = await telegram_adapter.get_wallet_balance(user_id)

    return (
        "💳 *Deposit to FanPesa*\n\n"
        f"Current balance: *{balance.balance:,.2f} {balance.currency}*\n\n"
        "Deposits are made securely inside the FanPesa Mini App. "
        "Tap below to open it and choose a payment method."
    )


async def deposit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current balance and direct the user to the Mini App to deposit."""
    user = update.effective_user
    if user is None or update.message is None:
        return

    logger.info("action=deposit user_id=%s username=%s", user.id, user.username)

    text = await build_deposit_text(user.id)

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=wallet_keyboard(),
    )


DEPOSIT_BUTTON_TEXT = Buttons.DEPOSIT
