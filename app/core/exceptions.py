"""
FanPesa Telegram Bot Exceptions

Centralized application exceptions.

Never raise generic Exception unless absolutely necessary.
"""

from __future__ import annotations


class FanPesaError(Exception):
    """
    Base exception for the FanPesa application.

    All custom exceptions should inherit from this class.
    """

    default_message = "An unexpected FanPesa error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


# =============================================================================
# Configuration
# =============================================================================


class ConfigurationError(FanPesaError):
    default_message = "Application configuration is invalid."


# =============================================================================
# Authentication
# =============================================================================


class AuthenticationError(FanPesaError):
    default_message = "Authentication failed."


class AuthorizationError(FanPesaError):
    default_message = "User is not authorized."


# =============================================================================
# Telegram
# =============================================================================


class TelegramBotError(FanPesaError):
    default_message = "Telegram Bot error."


class TelegramWebhookError(TelegramBotError):
    default_message = "Telegram webhook failed."


class TelegramAPIError(TelegramBotError):
    default_message = "Telegram API request failed."


# =============================================================================
# Backend API
# =============================================================================


class APIError(FanPesaError):
    default_message = "Backend API error."


class APIConnectionError(APIError):
    default_message = "Unable to connect to FanPesa API."


class APITimeoutError(APIError):
    default_message = "FanPesa API request timed out."


class APIValidationError(APIError):
    default_message = "FanPesa API validation failed."


# =============================================================================
# Wallet
# =============================================================================


class WalletError(FanPesaError):
    default_message = "Wallet operation failed."


class InsufficientFundsError(WalletError):
    default_message = "Insufficient wallet balance."


class DepositError(WalletError):
    default_message = "Deposit failed."


class WithdrawalError(WalletError):
    default_message = "Withdrawal failed."


# =============================================================================
# Betting
# =============================================================================


class BettingError(FanPesaError):
    default_message = "Betting operation failed."


class InvalidBetError(BettingError):
    default_message = "Invalid betting request."


# =============================================================================
# Promotions
# =============================================================================


class PromotionError(FanPesaError):
    default_message = "Promotion service unavailable."


# =============================================================================
# Validation
# =============================================================================


class ValidationError(FanPesaError):
    default_message = "Validation failed."


class InvalidInputError(ValidationError):
    default_message = "Invalid user input."


# =============================================================================
# Database
# =============================================================================


class DatabaseError(FanPesaError):
    default_message = "Database operation failed."


class DatabaseConnectionError(DatabaseError):
    default_message = "Unable to connect to the database."


# =============================================================================
# Redis
# =============================================================================


class RedisError(FanPesaError):
    default_message = "Redis operation failed."


# =============================================================================
# Rate Limiting
# =============================================================================


class RateLimitExceeded(FanPesaError):
    default_message = "Rate limit exceeded."


# =============================================================================
# Feature Flags
# =============================================================================


class FeatureUnavailable(FanPesaError):
    default_message = "This feature is currently unavailable."
