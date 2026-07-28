"""
Inline keyboards for FanPesa Telegram Bot.

Every button here is a `web_app` (opens the Mini App inside Telegram)
or a `tg://` deep link (opens a Telegram chat) — none of them need a
`CallbackQueryHandler` or a backend call, since Telegram resolves
both button types entirely client-side.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.config.settings import settings
from app.core.constants import SUPPORT_PHONE_TELEGRAM

SUPPORT_CHAT_URL = f"tg://resolve?phone={SUPPORT_PHONE_TELEGRAM}"


def _web_app_button(text: str, url: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))


def launch_app_keyboard() -> InlineKeyboardMarkup:
    """Primary keyboard shown on /start — every action stays inside Telegram."""

    keyboard = [
        [_web_app_button("🚀 Open FanPesa", settings.webapp_url)],
        [
            _web_app_button("📝 Register", settings.register_url),
            _web_app_button("🔐 Login", settings.login_url),
        ],
        [
            _web_app_button("💳 Deposit", settings.deposit_url),
            _web_app_button("💸 Withdraw", settings.withdraw_url),
        ],
        [
            InlineKeyboardButton("🛟 Contact Support", url=SUPPORT_CHAT_URL),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def support_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside the support message."""

    keyboard = [
        [InlineKeyboardButton("🛟 Message Support", url=SUPPORT_CHAT_URL)],
    ]

    return InlineKeyboardMarkup(keyboard)
