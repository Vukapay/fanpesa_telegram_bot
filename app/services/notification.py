"""
Notification Service

Central place to format and dispatch user notifications. Actual
delivery is platform-specific (Telegram message, browser push,
OneApp notification) and is performed by the calling platform
adapter; this service is the future integration point for a shared
notification backend (e.g. queued via Redis).
"""

from __future__ import annotations

from app.core.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Business-level notification formatting and audit logging."""

    async def notify(self, user_id: int, message: str) -> None:
        """
        Record that a notification was sent to a user.

        Platform adapters are responsible for the actual delivery
        (e.g. `Bot.send_message` for Telegram); this method is the
        hook for future shared notification infrastructure.
        """
        logger.info("Notification dispatched to user_id=%s: %s", user_id, message)


notification_service = NotificationService()
