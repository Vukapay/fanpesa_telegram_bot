"""
Inline keyboards for FanPesa Telegram Bot.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.config.settings import settings
from app.core.constants import CallbackData


def _open_app_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="🚀 Open FanPesa",
        web_app=WebAppInfo(url=settings.webapp_url),
    )


def launch_app_keyboard() -> InlineKeyboardMarkup:
    """Primary keyboard shown on /start: launch button + quick actions."""

    keyboard = [
        [_open_app_button()],
        [
            InlineKeyboardButton("💰 Wallet", callback_data=CallbackData.WALLET),
            InlineKeyboardButton("🎁 Promotions", callback_data=CallbackData.PROMOTIONS),
        ],
        [
            InlineKeyboardButton("💳 Deposit", callback_data=CallbackData.DEPOSIT),
            InlineKeyboardButton("💸 Withdraw", callback_data=CallbackData.WITHDRAW),
        ],
        [
            InlineKeyboardButton("🛟 Support", callback_data=CallbackData.SUPPORT),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def wallet_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside wallet balance/transaction messages."""

    keyboard = [
        [_open_app_button()],
        [InlineKeyboardButton("🔙 Back to menu", callback_data=CallbackData.OPEN_APP)],
    ]

    return InlineKeyboardMarkup(keyboard)


def promotions_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside the promotions list."""

    keyboard = [[_open_app_button()]]

    return InlineKeyboardMarkup(keyboard)


def support_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside the support message."""

    keyboard = [
        [InlineKeyboardButton("🛟 Contact Support", url="https://www.fanpesa.com")],
    ]

    return InlineKeyboardMarkup(keyboard)
