"""A custom caching decorator for async methods with LRU eviction."""

import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

P = ParamSpec("P")
T = TypeVar("T")

# Default maximum cache size to prevent unbounded memory growth
DEFAULT_CACHE_MAXSIZE = 128


def async_timed_cache(
    timeout: int = 300,
    maxsize: int = DEFAULT_CACHE_MAXSIZE,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Decorate to cache the result of an async method on an instance.

    The cache is stored on the instance itself and has a timeout.
    LRU eviction is applied when the cache exceeds maxsize.

    Args:
    ----
        timeout: The cache timeout in seconds.
        maxsize: Maximum number of entries to keep in cache. When exceeded,
                 the least recently used entries are evicted. Set to 0 for
                 unlimited size (not recommended for long-running instances).

    Returns
    -------
        The decorator.

    """

    def decorator(
        func: Callable[..., Awaitable[T]],
    ) -> Callable[..., Awaitable[T]]:
        """Return the decorator."""

        @wraps(func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
            """Wrap the original function."""
            if not hasattr(self, "_cache_storage"):
                object.__setattr__(self, "_cache_storage", {})
            if not hasattr(self, "_cache_last_update"):
                object.__setattr__(self, "_cache_last_update", {})
            if not hasattr(self, "_cache_access_order"):
                object.__setattr__(self, "_cache_access_order", [])

            # Create a unique key for the function call
            key_parts = [func.__name__]
            if args:
                key_parts.extend(str(a) for a in args)
            if kwargs:
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # Check if a valid cache entry exists
            if cache_key in self._cache_storage:
                last_update = self._cache_last_update.get(cache_key, 0)
                if time.time() - last_update < timeout:
                    # Update access order for LRU tracking
                    if cache_key in self._cache_access_order:
                        self._cache_access_order.remove(cache_key)
                    self._cache_access_order.append(cache_key)
                    return cast(T, self._cache_storage[cache_key])
                # Entry has expired, remove it
                del self._cache_storage[cache_key]
                del self._cache_last_update[cache_key]
                if cache_key in self._cache_access_order:
                    self._cache_access_order.remove(cache_key)

            # Apply LRU eviction if cache is at capacity
            if maxsize > 0:
                while len(self._cache_storage) >= maxsize:
                    if self._cache_access_order:
                        oldest_key = self._cache_access_order.pop(0)
                        self._cache_storage.pop(oldest_key, None)
                        self._cache_last_update.pop(oldest_key, None)
                    else:
                        # Fallback: clear first item if access order is empty
                        if self._cache_storage:
                            first_key = next(iter(self._cache_storage))
                            del self._cache_storage[first_key]
                            self._cache_last_update.pop(first_key, None)
                        break

            # Call the original function and cache the result
            result = await func(self, *args, **kwargs)
            self._cache_storage[cache_key] = result
            self._cache_last_update[cache_key] = time.time()
            self._cache_access_order.append(cache_key)
            return result

        return wrapper

    return decorator
