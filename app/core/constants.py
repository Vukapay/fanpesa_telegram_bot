"""
FanPesa Telegram Bot Constants

Application-wide constants.

Never hardcode reusable strings throughout the application.
"""

from __future__ import annotations

# =============================================================================
# COMPANY / SUPPORT
# =============================================================================

COMPANY_NAME = "FanPesa"

WEBSITE = "https://www.fanpesa.com"

# Support email/phone are configured via .env — see app/config/settings.py
# (support_email, support_phone).

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
