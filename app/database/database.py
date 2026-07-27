"""
Database / Cache Layer

Redis is provisioned for future use (session caching, rate limiting,
idempotency keys for deposits/withdrawals). No relational database
is required for this milestone since all data is served by the
mock API; this wrapper exists so services can start depending on a
cache without any code changes once Redis is actually used.
"""

from __future__ import annotations

import redis.asyncio as redis

from app.config.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Thin async Redis wrapper. Connects lazily on first use."""

    def __init__(self, url: str | None = None) -> None:
        self._url = url or settings.redis_url
        self._client: redis.Redis | None = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.from_url(self._url, decode_responses=True)
        return self._client

    async def ping(self) -> bool:
        """Check connectivity to Redis, returning False instead of raising."""
        try:
            return await self.client.ping()
        except Exception:
            logger.warning("Redis is not reachable at %s", self._url)
            return False

    async def close(self) -> None:
        """Close the underlying Redis connection, if one was opened."""
        if self._client is not None:
            await self._client.aclose()


database = Database()
