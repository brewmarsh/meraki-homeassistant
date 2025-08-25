"""Module for asynchronous logging utilities."""

import logging
from typing import Any, Callable
import asyncio
from functools import wraps


def async_log_time(
    logger: logging.Logger, level: int = logging.INFO
) -> Callable[..., Any]:
    """Decorate to log the execution time of an async function."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = asyncio.get_event_loop().time()
            result = await func(*args, **kwargs)
            end_time = asyncio.get_event_loop().time()
            logger.log(
                level,
                "Execution of %s took %.4f seconds",
                func.__name__,
                end_time - start_time,
            )
            return result

        return wrapper

    return decorator
