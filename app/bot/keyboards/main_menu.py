"""
Persistent reply keyboard for the FanPesa Telegram Bot.
"""

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from app.config.settings import settings


def main_menu() -> ReplyKeyboardMarkup:
    """Persistent menu: Open FanPesa, Aviator, Register, Login, Deposit, Withdraw, Support, Promotion.

    Open FanPesa/Aviator/Register/Login/Deposit/Withdraw/Promotion open
    the Mini App directly (`web_app`) — tapping them never sends a
    message back to the bot, so no handler is registered for them.
    Support does send a message, since it replies with bot-side content.
    """

    keyboard = [
        [
            KeyboardButton(
                "🚀 Open FanPesa",
                web_app=WebAppInfo(url=settings.webapp_url),
            ),
        ],
        [
            KeyboardButton(
                "✈️ Aviator",
                web_app=WebAppInfo(url=settings.aviator_url),
            ),
        ],
        [
            KeyboardButton(
                "📝 Register",
                web_app=WebAppInfo(url=settings.register_url),
            ),
            KeyboardButton(
                "🔐 Login",
                web_app=WebAppInfo(url=settings.login_url),
            ),
        ],
        [
            KeyboardButton(
                "💳 Deposit",
                web_app=WebAppInfo(url=settings.deposit_url),
            ),
            KeyboardButton(
                "💸 Withdraw",
                web_app=WebAppInfo(url=settings.withdraw_url),
            ),
        ],
        [
            KeyboardButton("🛟 Support"),
            KeyboardButton(
                "🎁 Promotion",
                web_app=WebAppInfo(url=settings.promotion_url),
            ),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )
