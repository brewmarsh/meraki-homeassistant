"""API utility functions."""

import asyncio
import functools
import logging
from typing import Any, Callable, Dict, TypeVar, cast
from aiohttp import ClientError
from meraki.exceptions import APIError  # type: ignore

from ..errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiNetworkError,
)

# Type variable for generic function return type
T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)


def handle_meraki_errors(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle Meraki API errors consistently.

    This decorator:
    1. Converts Meraki exceptions to our custom exceptions
    2. Adds logging for API errors
    3. Includes proper rate limit handling

    Args:
        func: The API function to wrap

    Returns:
        Wrapped function with error handling
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        """Wrap the API function with error handling."""
        try:
            return await func(*args, **kwargs)
        except APIError as err:
            if _is_informational_error(err):
                _LOGGER.debug("Informational Meraki API condition: %s", err)
                raise MerakiNetworkError(f"Informational error: {err}")

            _LOGGER.error("Meraki API error: %s", err)
            if _is_auth_error(err):
                raise MerakiAuthenticationError(f"Authentication failed: {err}")
            elif _is_device_error(err):
                raise MerakiDeviceError(f"Device error: {err}")
            elif _is_network_error(err):
                raise MerakiNetworkError(f"Network error: {err}")
            elif _is_rate_limit_error(err):
                # Wait and retry for rate limit errors
                _LOGGER.warning("Rate limit exceeded, retrying in 2 seconds...")
                await asyncio.sleep(2)
                return await wrapper(*args, **kwargs)
            else:
                raise MerakiConnectionError(f"API error: {err}")
        except ClientError as err:
            _LOGGER.error("Connection error: %s", err)
            raise MerakiConnectionError(f"Connection error: {err}")
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            raise MerakiConnectionError(f"Unexpected error: {err}")

    return cast(Callable[..., T], wrapper)


def _is_rate_limit_error(err: APIError) -> bool:
    """Check if error is due to rate limiting."""
    return getattr(err, "status", None) == 429 or "rate limit" in str(err).lower()


def _is_auth_error(err: APIError) -> bool:
    """Check if error is an authentication error."""
    return getattr(err, "status", None) in (401, 403) or any(
        msg in str(err).lower()
        for msg in [
            "unauthorized",
            "forbidden",
            "invalid api key",
            "authentication failed",
        ]
    )


def _is_device_error(err: APIError) -> bool:
    """Check if error is device-related."""
    return any(
        msg in str(err).lower()
        for msg in [
            "device not found",
            "invalid serial",
            "device error",
            "device offline",
        ]
    )


def _is_network_error(err: APIError) -> bool:
    """Check if error is network-related."""
    return any(
        msg in str(err).lower()
        for msg in [
            "network not found",
            "invalid network",
            "network error",
            "network offline",
        ]
    )


def _is_informational_error(err: APIError) -> bool:
    """Check if error is informational (e.g., feature not enabled)."""
    error_str = str(err).lower()
    return "vlans are not enabled" in error_str or "traffic analysis" in error_str


def validate_response(response: Any) -> Dict[str, Any]:
    """Validate and normalize an API response.

    Args:
        response: The API response to validate

    Returns:
        Normalized response dictionary

    Raises:
        MerakiConnectionError: If response is invalid or empty
    """
    if response is None:
        _LOGGER.warning("Empty response from API")
        raise MerakiConnectionError("Empty response from API")

    if isinstance(response, dict):
        if not response:  # Empty dict
            _LOGGER.warning("Empty response dictionary")
            raise MerakiConnectionError("Empty response dictionary")
        return response

    if isinstance(response, list):
        # Lists are common responses, return them as is
        return response

    if isinstance(response, (str, int, float, bool)):
        # Single values should be wrapped in a proper structure
        return {"value": response}

    _LOGGER.warning(
        "Invalid response format: %s. Expected dict or list.", type(response)
    )
    raise MerakiConnectionError(
        f"Invalid response format: {type(response)}. Expected dict or list."
    )
