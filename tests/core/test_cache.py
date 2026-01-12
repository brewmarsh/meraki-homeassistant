"""Tests for the async_timed_cache decorator."""

import asyncio

import pytest

from custom_components.meraki_ha.core.api.cache import async_timed_cache


class MockClient:
    """Mock client class for testing the cache decorator."""

    def __init__(self) -> None:
        """Initialize the mock client."""
        self.call_count = 0

    @async_timed_cache(timeout=1)
    async def fetch_data(self, key: str) -> str:
        """Fetch data with caching."""
        self.call_count += 1
        return f"result_{key}"

    @async_timed_cache(timeout=60, maxsize=3)
    async def fetch_with_limit(self, key: str) -> str:
        """Fetch data with limited cache size."""
        self.call_count += 1
        return f"result_{key}"


class TestAsyncTimedCache:
    """Tests for async_timed_cache decorator."""

    @pytest.mark.asyncio
    async def test_cache_returns_cached_value(self) -> None:
        """Test that cached value is returned on subsequent calls."""
        client = MockClient()

        # First call should execute the function
        result1 = await client.fetch_data("test")
        assert result1 == "result_test"
        assert client.call_count == 1

        # Second call should use cache
        result2 = await client.fetch_data("test")
        assert result2 == "result_test"
        assert client.call_count == 1  # No additional call

    @pytest.mark.asyncio
    async def test_cache_different_keys(self) -> None:
        """Test that different keys are cached separately."""
        client = MockClient()

        result1 = await client.fetch_data("key1")
        result2 = await client.fetch_data("key2")

        assert result1 == "result_key1"
        assert result2 == "result_key2"
        assert client.call_count == 2

    @pytest.mark.asyncio
    async def test_cache_expires_after_timeout(self) -> None:
        """Test that cache expires after timeout."""
        client = MockClient()

        # First call
        await client.fetch_data("test")
        assert client.call_count == 1

        # Wait for cache to expire (timeout is 1 second)
        await asyncio.sleep(1.1)

        # Should execute function again
        await client.fetch_data("test")
        assert client.call_count == 2

    @pytest.mark.asyncio
    async def test_lru_eviction_when_maxsize_exceeded(self) -> None:
        """Test that LRU eviction occurs when maxsize is exceeded."""
        client = MockClient()

        # Fill the cache (maxsize=3)
        await client.fetch_with_limit("a")
        await client.fetch_with_limit("b")
        await client.fetch_with_limit("c")
        assert client.call_count == 3

        # These should all be cached
        await client.fetch_with_limit("a")
        await client.fetch_with_limit("b")
        await client.fetch_with_limit("c")
        assert client.call_count == 3  # Still 3, using cache

        # Adding a 4th key should evict the least recently used (a)
        await client.fetch_with_limit("d")
        assert client.call_count == 4

        # Key 'd' should be cached
        await client.fetch_with_limit("d")
        assert client.call_count == 4

        # Key 'a' was evicted, should need to fetch again
        await client.fetch_with_limit("a")
        assert client.call_count == 5

    @pytest.mark.asyncio
    async def test_lru_updates_access_order(self) -> None:
        """Test that accessing a cached item updates its LRU position."""
        client = MockClient()

        # Fill the cache (maxsize=3)
        await client.fetch_with_limit("a")  # LRU order: [a]
        await client.fetch_with_limit("b")  # LRU order: [a, b]
        await client.fetch_with_limit("c")  # LRU order: [a, b, c]
        assert client.call_count == 3

        # Access 'a' to move it to most recently used
        await client.fetch_with_limit("a")  # LRU order: [b, c, a]
        assert client.call_count == 3  # Still cached

        # Add 'd' - should evict 'b' (now the least recently used)
        await client.fetch_with_limit("d")  # LRU order: [c, a, d], b evicted
        assert client.call_count == 4

        # 'a' should still be cached (wasn't evicted)
        await client.fetch_with_limit("a")
        assert client.call_count == 4

        # 'b' was evicted, should need to fetch again
        await client.fetch_with_limit("b")
        assert client.call_count == 5

    @pytest.mark.asyncio
    async def test_cache_with_kwargs(self) -> None:
        """Test that kwargs are included in cache key."""
        client = MockClient()

        @async_timed_cache(timeout=60)
        async def fetch_with_options(self, key: str, option: str = "default") -> str:
            self.call_count += 1
            return f"{key}_{option}"

        # Bind method to client (dynamic attribute assignment)
        client.fetch_with_options = fetch_with_options.__get__(  # type: ignore[attr-defined]
            client, type(client)
        )

        result1 = await client.fetch_with_options("test", option="a")  # type: ignore[attr-defined]
        result2 = await client.fetch_with_options("test", option="b")  # type: ignore[attr-defined]
        result3 = await client.fetch_with_options("test", option="a")  # type: ignore[attr-defined]

        assert result1 == "test_a"
        assert result2 == "test_b"
        assert result3 == "test_a"
        assert client.call_count == 2  # Third call used cache
