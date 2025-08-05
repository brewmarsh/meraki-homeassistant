"""A custom caching decorator for async methods."""
from functools import wraps
import time
from typing import Any, Dict

def async_timed_cache(timeout: int = 300):

    """
    Decorator to cache the result of an async method on an instance with a timeout.
    The cache is stored on the instance itself.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not hasattr(self, '_cache_storage'):
                self._cache_storage: Dict[str, Any] = {}
            if not hasattr(self, '_cache_last_update'):
                self._cache_last_update: Dict[str, float] = {}

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
                    return self._cache_storage[cache_key]

            # If not, call the original function and cache the result
            result = await func(self, *args, **kwargs)
            self._cache_storage[cache_key] = result
            self._cache_last_update[cache_key] = time.time()
            return result
        return wrapper
    return decorator
