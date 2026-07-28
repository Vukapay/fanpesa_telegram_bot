"""
FanPesa Telegram Bot Constants

Application-wide constants.

Never hardcode reusable strings throughout the application.
"""

from __future__ import annotations

from enum import StrEnum

# =============================================================================
# APPLICATION
# =============================================================================

APP_NAME = "FanPesa Telegram Bot"

APP_VERSION = "1.0.0"

COMPANY_NAME = "FanPesa"

WEBSITE = "https://www.fanpesa.com"

SUPPORT_EMAIL = "support@fanpesa.com"

SUPPORT_PHONE_DISPLAY = "+254 745 275 966"

# Digits-only, no leading "+" — required by Telegram's tg://resolve?phone= deep link.
SUPPORT_PHONE_TELEGRAM = "254745275966"

# =============================================================================
# TELEGRAM
# =============================================================================

BOT_USERNAME = "fanpesa_bot"

MINI_APP_NAME = "FanPesa Telegram App"

WEB_APP_URL = WEBSITE

# =============================================================================
# COMMANDS
# =============================================================================

START_COMMAND = "start"

HELP_COMMAND = "help"

ABOUT_COMMAND = "about"

SUPPORT_COMMAND = "support"

WALLET_COMMAND = "wallet"

PROMOTIONS_COMMAND = "promotions"

DEPOSIT_COMMAND = "deposit"

WITHDRAW_COMMAND = "withdraw"

REFERRAL_COMMAND = "referral"

# =============================================================================
# PLATFORM
# =============================================================================


class Platform(StrEnum):
    """Supported FanPesa platforms."""

    TELEGRAM = "telegram"

    WEB = "web"

    ONEAPP = "oneapp"

    API = "api"


# =============================================================================
# ENVIRONMENTS
# =============================================================================


class Environment(StrEnum):
    DEVELOPMENT = "development"

    STAGING = "staging"

    PRODUCTION = "production"


# =============================================================================
# LOGGING
# =============================================================================


class LogMessage:
    APPLICATION_STARTING = "Application starting"

    APPLICATION_STOPPED = "Application stopped"

    BOT_INITIALIZED = "Telegram bot initialized"

    BOT_CONNECTED = "Telegram bot connected"

    API_CONNECTED = "Backend API connected"

    API_DISCONNECTED = "Backend API disconnected"

    USER_LOGIN = "User authenticated"

    USER_LOGOUT = "User logged out"

    ERROR = "Unexpected application error"


# =============================================================================
# DEFAULT RESPONSES
# =============================================================================


class Messages:

    WELCOME = (
        "🎉 Welcome to FanPesa!\n\n"
        "Your secure gaming wallet inside Telegram.\n\n"
        "Use the menu below to get started."
    )

    HELP = "Need assistance?\n\n" "Use the available commands or contact FanPesa Support."

    UNDER_CONSTRUCTION = "🚧 This feature is currently under development."

    API_UNAVAILABLE = "⚠️ FanPesa services are temporarily unavailable."


# =============================================================================
# BUTTON LABELS
# =============================================================================


class Buttons:

    OPEN_APP = "🚀 Open FanPesa"

    REGISTER = "📝 Register"

    LOGIN = "🔐 Login"

    DEPOSIT = "💳 Deposit"

    WITHDRAW = "💸 Withdraw"

    SUPPORT = "🛟 Support"

    PROMOTION = "🎁 Promotion"

    INVITE = "👥 Invite Friends"


# =============================================================================
# API ROUTES
# =============================================================================


class ApiRoutes:

    AUTH = "/api/v1/auth"

    PROFILE = "/api/v1/profile"

    WALLET = "/api/v1/wallet"

    DEPOSIT = "/api/v1/deposit"

    WITHDRAW = "/api/v1/withdraw"

    PROMOTIONS = "/api/v1/promotions"

    REFERRALS = "/api/v1/referrals"


# =============================================================================
# HEALTH
# =============================================================================

HEALTH_ENDPOINT = "/health"

API_VERSION_ENDPOINT = "/version"
