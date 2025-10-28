"""Module for asynchronous logging utilities."""
import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def async_log_time(
    logger: logging.Logger,
    level: int = logging.INFO,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorate to log the execution time of an async function.

    Args:
    ----
        logger: The logger to use for logging.
        level: The logging level to use.

    Returns
    -------
        The decorator.

    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Return the decorator function."""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap the function and logs the execution time."""
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
