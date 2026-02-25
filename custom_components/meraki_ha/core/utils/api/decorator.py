"""API error handling decorator."""

import functools
import logging
from collections.abc import Awaitable, Callable, Coroutine
from json import JSONDecodeError
from typing import Any, TypeVar, cast

from aiohttp import ClientError
from meraki.exceptions import APIError  # type: ignore

from ...errors import MerakiConnectionError, MerakiInformationalError
from .errors import RetryRequest
from .handlers import (
    handle_api_exception,
    handle_invalid_response_error,
    handle_unexpected_error,
)

# Type variable for generic function return type
T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)


def handle_meraki_errors(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Coroutine[Any, Any, T]]:
    """Decorate to handle Meraki API errors consistently."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        """Wrap the API function with error handling."""
        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries + 1):
            try:
                return await _execute_api_call(
                    func, args, kwargs, (attempt, max_retries, base_delay)
                )
            except RetryRequest:
                continue

        return cast(T, {})

    return cast(Callable[..., Coroutine[Any, Any, T]], wrapper)


async def _execute_api_call(
    func: Callable[..., Awaitable[T]],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    retry_context: tuple[int, int, int],
) -> T:
    """Execute a single API call and handle exceptions."""
    try:
        return await func(*args, **kwargs)
    except (JSONDecodeError, MerakiConnectionError) as err:
        return cast(T, handle_invalid_response_error(func, err))
    except (APIError, MerakiInformationalError) as err:
        return cast(
            T,
            await handle_api_exception(err, func, args, kwargs, retry_context),
        )
    except ClientError as err:
        _LOGGER.error("Connection error: %s", err)
        raise MerakiConnectionError(f"Connection error: {err}") from err
    except Exception as err:
        handle_unexpected_error(err)
        return cast(T, {})
