"""
Inline keyboards for FanPesa Telegram Bot.

Every button here is a `web_app` (opens the Mini App inside Telegram)
or a `tg://` deep link (opens a Telegram chat) — none of them need a
`CallbackQueryHandler` or a backend call, since Telegram resolves
both button types entirely client-side.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.config.settings import settings


def _support_chat_url() -> str:
    return f"tg://resolve?phone={settings.support_phone_telegram}"


def _web_app_button(text: str, url: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))


def launch_app_keyboard() -> InlineKeyboardMarkup:
    """Primary keyboard shown on /start — every action stays inside Telegram."""

    keyboard = [
        [_web_app_button("🚀 Open FanPesa", settings.webapp_url)],
        [_web_app_button("✈️ Play Aviator 🔥", settings.aviator_url)],
        [
            _web_app_button("📝 Register", settings.register_url),
            _web_app_button("🔐 Login", settings.login_url),
        ],
        [
            _web_app_button("💳 Deposit", settings.deposit_url),
            _web_app_button("💸 Withdraw", settings.withdraw_url),
        ],
        [
            InlineKeyboardButton("🛟 Contact Support", url=_support_chat_url()),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def support_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside the support message."""

    keyboard = [
        [InlineKeyboardButton("🛟 Message Support", url=_support_chat_url())],
    ]

    return InlineKeyboardMarkup(keyboard)


def aviator_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown alongside the Aviator promo message."""

    keyboard = [
        [_web_app_button("✈️ Play Aviator Now 🔥", settings.aviator_url)],
    ]

    return InlineKeyboardMarkup(keyboard)
