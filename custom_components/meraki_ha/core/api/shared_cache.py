"""Shared cache for Meraki API requests to prevent thundering herd."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, TypeVar

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


class MerakiApiCache:
    """
    A thread-safe, lock-backed API cache.

    This class implements the double-checked locking pattern to prevent
    the 'thundering herd' problem where multiple concurrent requests
    bypass an empty cache and all hit the API.
    """

    def __init__(self, ttl: int = 45) -> None:
        """Initialize the cache."""
        self._cache: dict[str, dict[str, Any]] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._ttl = ttl

    async def async_get_or_fetch(
        self, key: str, fetch_coro: Any, ttl: int | None = None
    ) -> Any:
        """
        Fetch data safely preventing the thundering herd.

        Args:
            key: The unique cache key for this request.
            fetch_coro: The coroutine or awaitable to fetch fresh data.
            ttl: Optional override for the TTL.

        Returns
        -------
            The cached or freshly fetched data.
        """
        target_ttl = ttl if ttl is not None else self._ttl

        # Action 6: Fast path - check if it's already cached and valid
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry["timestamp"] < target_ttl:
                return entry["data"]

        # Action 5: Ensure a lock exists for this key
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()

        # Action 6: Acquire the lock for that specific endpoint
        async with self._locks[key]:
            # Action 7: Double-check cache inside the lock
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry["timestamp"] < target_ttl:
                    _LOGGER.debug(
                        "Serving %s from shared cache (prevented thundering herd)", key
                    )
                    return entry["data"]

            _LOGGER.debug("Fetching fresh data for %s", key)

            # If fetch_coro is a callable, call it. If it's an awaitable, await it.
            if callable(fetch_coro):
                data = await fetch_coro()
            else:
                data = await fetch_coro

            # Action 7: Store the result in the cache and release the lock
            # (via context manager)
            self._cache[key] = {"timestamp": time.time(), "data": data}
            return data

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()
        self._locks.clear()
