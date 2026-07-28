"""
Application settings.

All configuration is loaded from environment variables.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------
    # App
    # -------------------------------------------------

    app_name: str = Field(default="FanPesa Telegram Bot")
    app_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # -------------------------------------------------
    # Telegram
    # -------------------------------------------------

    bot_token: str = Field(default="CHANGE_ME")

    webhook_url: str | None = None

    webapp_url: str = Field(default="https://www.fanpesa.com")

    register_url: str = Field(default="https://www.fanpesa.com/register")
    login_url: str = Field(default="https://www.fanpesa.com/login")
    deposit_url: str = Field(default="https://www.fanpesa.com/deposit")
    withdraw_url: str = Field(default="https://www.fanpesa.com/withdrawal")
    promotion_url: str = Field(default="https://www.fanpesa.com/promotion")

    # -------------------------------------------------
    # Support
    # -------------------------------------------------

    support_email: str = Field(default="support@fanpesa.com")
    support_phone: str = Field(default="+254 745 275 966")

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    log_level: str = Field(default="INFO")

    @property
    def support_phone_telegram(self) -> str:
        """Digits-only phone number for Telegram's `tg://resolve?phone=` deep link."""
        return "".join(char for char in self.support_phone if char.isdigit())


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""

    return Settings()


settings = get_settings()
