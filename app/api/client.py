"""
HTTP Client for the FanPesa Backend

Thin async wrapper around `httpx.AsyncClient`. This is the single
place network calls to the real FanPesa backend will be made from
once it becomes available — the service layer depends on this
interface, not on `httpx` directly.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.config.settings import settings
from app.core.exceptions import APIConnectionError
from app.core.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT_SECONDS = 30.0


class APIClient:
    """Async HTTP client for calling FanPesa backend APIs."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url or settings.api_base_url,
            timeout=timeout,
        )

    async def get(self, endpoint: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Perform a GET request against the backend API."""
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: dict[str, Any] | None = None) -> httpx.Response:
        """Perform a POST request against the backend API."""
        return await self._request("POST", endpoint, json=json)

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        try:
            response = await self._client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as exc:
            logger.error("API request failed: %s %s (%s)", method, endpoint, exc)
            raise APIConnectionError(f"Request to {endpoint} failed: {exc}") from exc

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.aclose()

    async def __aenter__(self) -> APIClient:
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.close()


api_client = APIClient()
