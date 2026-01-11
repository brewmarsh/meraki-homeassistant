"""Module for asynchronous logging utilities.

Provides decorators for timing async operations. Use sparingly on
performance-critical paths like API calls and coordinator refreshes.

Example usage:
    from custom_components.meraki_ha.async_logging import async_log_time
    from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

    @async_log_time()  # Uses MerakiLoggers.API by default
    async def fetch_devices(self):
        ...

    @async_log_time(MerakiLoggers.COORDINATOR)  # Use specific logger
    async def _async_update_data(self):
        ...
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

if TYPE_CHECKING:
    from typing import Final

P = ParamSpec("P")
R = TypeVar("R")

# Threshold in seconds - only log if operation takes longer than this
_SLOW_THRESHOLD: Final = 1.0


def async_log_time(
    logger: logging.Logger | None = None,
    level: int = logging.DEBUG,
    slow_threshold: float | None = None,
) -> Callable[
    [Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]
]:
    """Decorate to log the execution time of an async function.

    Use on performance-critical async operations to monitor timing.
    By default, only logs at DEBUG level to avoid noise.

    Parameters
    ----------
        logger: The logger to use. Defaults to MerakiLoggers.API.
        level: The logging level. Defaults to DEBUG.
        slow_threshold: If set, logs at WARNING level when execution
            exceeds this many seconds. Defaults to 1.0 seconds.

    Returns
    -------
        The decorator function.

    Example
    -------
        @async_log_time()
        async def get_organizations(self):
            return await self._dashboard.organizations.getOrganizations()

        @async_log_time(MerakiLoggers.COORDINATOR, slow_threshold=5.0)
        async def _async_update_data(self):
            ...

    """
    # Import here to avoid circular imports
    from .helpers.logging_helper import MerakiLoggers

    actual_logger = logger if logger is not None else MerakiLoggers.API
    threshold = slow_threshold if slow_threshold is not None else _SLOW_THRESHOLD

    def decorator(
        func: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        """Return the decorator function."""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap the function and log the execution time."""
            start_time = asyncio.get_event_loop().time()
            result = await func(*args, **kwargs)
            elapsed = asyncio.get_event_loop().time() - start_time

            # Log at WARNING level if slow, otherwise at specified level
            if elapsed >= threshold:
                actual_logger.warning(
                    "%s completed in %.3fs (slow, threshold: %.1fs)",
                    func.__name__,
                    elapsed,
                    threshold,
                )
            else:
                actual_logger.log(
                    level,
                    "%s completed in %.3fs",
                    func.__name__,
                    elapsed,
                )
            return result

        return wrapper

    return decorator
