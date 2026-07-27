"""
Wallet Handler

Responds to the "💰 Wallet" menu button by showing the user's
current balance and recent transactions, resolved through the
Telegram platform adapter (never directly from the service/API layer).
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.inline import wallet_keyboard
from app.core.constants import Buttons
from app.core.logger import get_logger
from app.platform.telegram import telegram_adapter

logger = get_logger(__name__)


async def build_wallet_text(user_id: int) -> str:
    """Render the wallet balance + recent transactions as a message body."""
    balance = await telegram_adapter.get_wallet_balance(user_id)
    transactions = await telegram_adapter.get_transaction_history(user_id)

    lines = [
        "💰 *Your FanPesa Wallet*",
        "",
        f"Available balance: *{balance.balance:,.2f} {balance.currency}*",
        f"Bonus balance: *{balance.bonus_balance:,.2f} {balance.currency}*",
        "",
        "Recent activity:",
    ]

    for transaction in transactions[:5]:
        lines.append(
            f"• {transaction.type.value.replace('_', ' ').title()} — {transaction.amount:,.2f}"
        )

    return "\n".join(lines)


async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's wallet balance and recent transactions."""
    user = update.effective_user
    if user is None or update.message is None:
        return

    logger.info("action=wallet user_id=%s username=%s", user.id, user.username)

    text = await build_wallet_text(user.id)

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=wallet_keyboard(),
    )


WALLET_BUTTON_TEXT = Buttons.WALLET
