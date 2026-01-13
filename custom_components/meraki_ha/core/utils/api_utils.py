"""API utility functions."""

import asyncio
import functools
import inspect
import logging
from collections.abc import Awaitable, Callable
from json import JSONDecodeError
from typing import Any, TypeVar, cast

from aiohttp import ClientError
from meraki.exceptions import APIError  # type: ignore

from ..errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiInformationalError,
    MerakiNetworkError,
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
)

# Type variable for generic function return type
T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)


def handle_meraki_errors(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """
    Decorate to handle Meraki API errors consistently.

    This decorator:
    1. Converts Meraki exceptions to our custom exceptions
    2. Adds logging for API errors
    3. Includes proper rate limit handling
    4. Handles empty/invalid responses by returning a type-safe empty value
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        """Wrap the API function with error handling."""
        try:
            return await func(*args, **kwargs)
        except (JSONDecodeError, MerakiConnectionError) as err:
            _LOGGER.warning(
                "API call %s failed with an empty or invalid response: %s",
                func.__name__,
                err,
            )
            # Inspect the wrapped function's return type to return a safe empty value
            sig = inspect.signature(func)
            return_type = sig.return_annotation
            if return_type is list or getattr(return_type, "__origin__", None) in (
                list,
                list,
            ):
                return cast(T, [])
            return cast(T, {})
        except APIError as err:
<<<<<<< HEAD
<<<<<<< HEAD
            if _is_informational_error(err):
                raise MerakiInformationalError(f"Informational error: {err}") from err
=======
<<<<<<< HEAD
            if _is_informational_error(err):
                raise MerakiInformationalError(f"Informational error: {err}") from err
=======
            _raise_if_informational_error(err)
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
            _raise_if_informational_error(err)
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

            _LOGGER.error("Meraki API error: %s", err)
            if _is_auth_error(err):
                raise MerakiAuthenticationError(
                    f"Authentication failed: {err}"
                ) from err
            elif _is_device_error(err):
                raise MerakiDeviceError(f"Device error: {err}") from err
            elif _is_network_error(err):
                raise MerakiNetworkError(f"Network error: {err}") from err
            elif _is_rate_limit_error(err):
                # Wait and retry for rate limit errors
                _LOGGER.warning("Rate limit exceeded, retrying in 2 seconds...")
                await asyncio.sleep(2)
                return await wrapper(*args, **kwargs)
            else:
                raise MerakiConnectionError(f"API error: {err}") from err
        except ClientError as err:
            _LOGGER.error("Connection error: %s", err)
            raise MerakiConnectionError(f"Connection error: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            raise MerakiConnectionError(f"Unexpected error: {err}") from err

    return cast(Callable[..., Awaitable[T]], wrapper)


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


<<<<<<< HEAD
<<<<<<< HEAD
def _is_informational_error(err: APIError) -> bool:
    """Check if error is informational (e.g., feature not enabled)."""
    error_str = str(err).lower()
    return (
        "vlans are not enabled" in error_str
        or "traffic analysis" in error_str
        or "historical viewing is not supported" in error_str
    )
=======
<<<<<<< HEAD
def _is_informational_error(err: APIError) -> bool:
    """Check if error is informational (e.g., feature not enabled)."""
    error_str = str(err).lower()
    return (
        "vlans are not enabled" in error_str
        or "traffic analysis" in error_str
        or "historical viewing is not supported" in error_str
    )
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
def _raise_if_informational_error(err: APIError) -> None:
    """
    Check if an API error is informational and raise a specific exception.

    Args:
        err: The APIError instance.

    Raises
    ------
        MerakiVlansDisabledError: If VLANs are not enabled.
        MerakiTrafficAnalysisError: If traffic analysis is not enabled.
        MerakiInformationalError: For other informational errors.
    """
    error_str = str(err).lower()
    if "vlans are not enabled" in error_str:
        raise MerakiVlansDisabledError(str(err)) from err
    if "traffic analysis" in error_str:
        raise MerakiTrafficAnalysisError(str(err)) from err
    if "historical viewing is not supported" in error_str:
        raise MerakiInformationalError(str(err)) from err
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


def validate_response(response: Any) -> dict[str, Any] | list[Any]:
    """
    Validate and normalize an API response.

    Args:
    ----
        response: The API response to validate

    Returns
    -------
        Normalized response dictionary

    Raises
    ------
        MerakiConnectionError: If response is invalid or empty

    """
    if response is None:
        raise MerakiConnectionError("Empty response from API")

    if isinstance(response, dict):
        if not response:
            _LOGGER.warning("Empty response dictionary from API")
        return response

    if isinstance(response, list):
        return response

    if isinstance(response, (str, int, float, bool)):
        return {"value": response}

    raise MerakiConnectionError(
        f"Invalid response format: {type(response)}. Expected dict or list."
    )
