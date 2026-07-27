"""
Persistent reply keyboard for the FanPesa Telegram Bot.
"""

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from app.config.settings import settings


def main_menu() -> ReplyKeyboardMarkup:
    """Persistent menu: Open FanPesa, Wallet, Promotions, Deposit, Withdraw, Support, About."""

    keyboard = [
        [
            KeyboardButton(
                "🚀 Open FanPesa",
                web_app=WebAppInfo(url=settings.webapp_url),
            ),
        ],
        [
            KeyboardButton("💰 Wallet"),
            KeyboardButton("🎁 Promotions"),
        ],
        [
            KeyboardButton("💳 Deposit"),
            KeyboardButton("💸 Withdraw"),
        ],
        [
            KeyboardButton("🛟 Support"),
            KeyboardButton("ℹ️ About"),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
