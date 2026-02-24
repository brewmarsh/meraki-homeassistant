"""API utility functions."""

import asyncio
import functools
import inspect
import logging
from collections.abc import Awaitable, Callable, Coroutine
from json import JSONDecodeError
from typing import Any, TypeVar, cast

from aiohttp import ClientError
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError  # type: ignore

from ..errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiInformationalError,
    MerakiNetworkError,
)

# Type variable for generic function return type
T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)

# Set of error messages that have already been logged as INFO to avoid flooding
_LOGGED_ERRORS: set[str] = set()


class _RetryRequest(Exception):
    """Internal exception to trigger a retry."""


def _get_safe_return_value(func: Callable[..., Any], error_msg: str | None = None) -> Any:
    """Get a safe return value based on the function's return type annotation."""
    sig = inspect.signature(func)
    return_type = sig.return_annotation
    if return_type is list or getattr(return_type, "__origin__", None) is list:
        return []
    if return_type is dict or getattr(return_type, "__origin__", None) is dict:
        return {}
    if error_msg:
        return MerakiInformationalError(error_msg)
    return {}


def _handle_invalid_response_error(func: Callable[..., Any], err: Exception) -> Any:
    """Handle empty or invalid responses."""
    _LOGGER.warning(
        "API call %s failed with an empty or invalid response: %s",
        func.__name__,
        err,
    )
    return _get_safe_return_value(func)


def _handle_feature_disabled(
    func: Callable[..., Any],
    err: Exception,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    """Handle disabled features by marking them in the client and returning safe value."""
    error_msg = str(err)
    is_traffic_analysis = "Traffic Analysis with Hostname Visibility" in error_msg

    _LOGGER.debug("Meraki feature disabled (skipping): %s", error_msg)

    # Attempt to mark the feature as disabled in the client session
    instance = args[0] if args else None
    client = getattr(instance, "_api_client", None)
    if client:
        # Extract network_id from arguments or keyword arguments
        network_id = kwargs.get("networkId") or kwargs.get("network_id")
        if not network_id and len(args) > 1:
            # network_id is typically the first argument after 'self'
            network_id = args[1]

        if network_id and isinstance(network_id, str):
            feature = "traffic" if is_traffic_analysis else "vlans"
            if hasattr(client, "mark_feature_disabled"):
                client.mark_feature_disabled(feature, network_id)

    return _get_safe_return_value(func, error_msg)


async def _handle_rate_limit(
    err: APIError, attempt: int, max_retries: int, base_delay: int
) -> None:
    """Handle rate limiting by sleeping and raising _RetryRequest."""
    if attempt >= max_retries:
        _LOGGER.error(
            "Meraki API rate limit reached after %s retries: %s",
            max_retries,
            err,
        )
        raise UpdateFailed(
            f"meraki.exceptions.APIError: 429 Too Many Requests "
            f"after {max_retries} retries"
        ) from err

    # Extract Retry-After if available
    delay = base_delay * (2**attempt)
    if isinstance(err, APIError) and hasattr(err, "response"):
        response = getattr(err, "response", None)
        if response and hasattr(response, "headers"):
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = float(retry_after)
                except (ValueError, TypeError):
                    pass

    _LOGGER.debug(
        "Meraki API rate limited (429). Waiting %s seconds before retry %s/%s",
        delay,
        attempt + 1,
        max_retries,
    )
    await asyncio.sleep(delay)
    raise _RetryRequest()


def _handle_meraki_api_error(err: APIError) -> None:
    """Handle standard Meraki API errors."""
    _LOGGER.error("Meraki API error: %s", err)
    if _is_auth_error(err):
        raise MerakiAuthenticationError(f"Authentication failed: {err}") from err
    elif _is_device_error(err):
        raise MerakiDeviceError(f"Device error: {err}") from err
    elif _is_network_error(err):
        raise MerakiNetworkError(f"Network error: {err}") from err
    else:
        raise MerakiConnectionError(f"API error: {err}") from err


def _handle_unexpected_error(err: Exception) -> None:
    """Handle unexpected exceptions."""
    if isinstance(err, UpdateFailed):
        raise err
    _LOGGER.error("Unexpected error: %s", err)
    raise MerakiConnectionError(f"Unexpected error: {err}") from err


async def _handle_api_exception(
    err: APIError | MerakiInformationalError,
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    retry_context: tuple[int, int, int],
) -> Any:
    """Handle APIError and MerakiInformationalError logic."""
    attempt, max_retries, base_delay = retry_context
    error_msg = str(err)
    is_feature_disabled = (
        "Traffic Analysis with Hostname Visibility" in error_msg
        or "VLANs are not enabled for this network" in error_msg
    )

    if is_feature_disabled:
        return _handle_feature_disabled(func, err, args, kwargs)

    if isinstance(err, APIError) and _is_informational_error(err):
        raise MerakiInformationalError(f"Informational error: {err}") from err

    if isinstance(err, MerakiInformationalError):
        raise err

    if isinstance(err, APIError) and _is_rate_limit_error(err):
        await _handle_rate_limit(err, attempt, max_retries, base_delay)

    _handle_meraki_api_error(cast(APIError, err))
    return None


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
                return await func(*args, **kwargs)
            except (JSONDecodeError, MerakiConnectionError) as err:
                return cast(T, _handle_invalid_response_error(func, err))
            except (APIError, MerakiInformationalError) as err:
                try:
                    return cast(
                        T,
                        await _handle_api_exception(
                            err, func, args, kwargs, (attempt, max_retries, base_delay)
                        ),
                    )
                except _RetryRequest:
                    continue
            except ClientError as err:
                _LOGGER.error("Connection error: %s", err)
                raise MerakiConnectionError(f"Connection error: {err}") from err
            except Exception as err:
                _handle_unexpected_error(err)

        return cast(T, {})

    return cast(Callable[..., Coroutine[Any, Any, T]], wrapper)


def validate_response(response: Any) -> Any:
    """Validate API response."""
    if response is None:
        raise MerakiConnectionError("API returned None")

    if isinstance(response, (dict, list)):
        return response

    # Wrap primitive types in a dict
    return {"value": response}


def _is_rate_limit_error(err: APIError) -> bool:
    """Check if the error is a rate limit error."""
    return getattr(err, "status", 0) == 429


def _is_auth_error(err: APIError) -> bool:
    """Check if the error is an authentication error."""
    return getattr(err, "status", 0) in (401, 403)


def _is_device_error(err: APIError) -> bool:
    """Check if the error is a device error."""
    if getattr(err, "status", 0) == 404:
        return True
    return "device not found" in str(err).lower()


def _is_network_error(err: APIError) -> bool:
    """Check if the error is a network error."""
    if getattr(err, "status", 0) == 404:
        return True
    return "network not found" in str(err).lower()


def _is_informational_error(err: APIError) -> bool:
    """Check if the error is informational."""
    return False
