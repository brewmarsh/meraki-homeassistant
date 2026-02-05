"""API utility functions."""

import asyncio
import functools
import inspect
import logging
from collections.abc import Awaitable, Callable, Coroutine
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
)

# Type variable for generic function return type
T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)

# Set of error messages that have already been logged as INFO to avoid flooding
_LOGGED_ERRORS: set[str] = set()


def handle_meraki_errors(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Coroutine[Any, Any, T]]:
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
        from homeassistant.helpers.update_coordinator import UpdateFailed

        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except (JSONDecodeError, MerakiConnectionError) as err:
                _LOGGER.warning(
                    "API call %s failed with an empty or invalid response: %s",
                    func.__name__,
                    err,
                )
                # Inspect return type to provide a safe empty value
                sig = inspect.signature(func)
                return_type = sig.return_annotation
                if (
                    return_type is list
                    or getattr(return_type, "__origin__", None) is list
                ):
                    return cast(T, [])
                return cast(T, {})
            except (APIError, MerakiInformationalError) as err:
                error_msg = str(err)
                is_traffic_analysis = (
                    "Traffic Analysis with Hostname Visibility" in error_msg
                )
                is_vlan_disabled = "VLANs are not enabled" in error_msg

                if is_traffic_analysis or is_vlan_disabled:
                    _LOGGER.debug("Meraki feature disabled (skipping): %s", error_msg)

                    # Attempt to mark the feature as disabled in the client session
                    # This prevents subsequent API calls for this feature
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

                    # Return a type-safe empty value instead of raising an error
                    sig = inspect.signature(func)
                    return_type = sig.return_annotation
                    if (
                        return_type is list
                        or getattr(return_type, "__origin__", None) is list
                    ):
                        return cast(T, [])
                    if (
                        return_type is dict
                        or getattr(return_type, "__origin__", None) is dict
                    ):
                        return cast(T, {})

                    # Return the error object as a last resort
                    # if return type is not list/dict
                    return cast(T, MerakiInformationalError(error_msg))

                if isinstance(err, APIError) and _is_informational_error(err):
                    raise MerakiInformationalError(
                        f"Informational error: {err}"
                    ) from err

                # Re-raise MerakiInformationalError if it was already raised
                # (e.g. by run_sync)
                if isinstance(err, MerakiInformationalError):
                    raise err

                if _is_rate_limit_error(err):
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
                        # Ensure response and headers exist (it might be a dict mock)
                        response = getattr(err, "response", None)
                        if response and hasattr(response, "headers"):
                            retry_after = response.headers.get("Retry-After")
                            if retry_after:
                                try:
                                    delay = float(retry_after)
                                except (ValueError, TypeError):
                                    pass

                    _LOGGER.debug(
                        "Meraki API rate limited (429). Waiting %s seconds before "
                        "retry %s/%s",
                        delay,
                        attempt + 1,
                        max_retries,
                    )
                    await asyncio.sleep(delay)
                    continue

                _LOGGER.error("Meraki API error: %s", err)
                if _is_auth_error(err):
                    raise MerakiAuthenticationError(
                        f"Authentication failed: {err}"
                    ) from err
                elif _is_device_error(err):
                    raise MerakiDeviceError(f"Device error: {err}") from err
                elif _is_network_error(err):
                    raise MerakiNetworkError(f"Network error: {err}") from err
                else:
                    raise MerakiConnectionError(f"API error: {err}") from err
            except ClientError as err:
                _LOGGER.error("Connection error: %s", err)
                raise MerakiConnectionError(f"Connection error: {err}") from err
            except Exception as err:
                # If it's already UpdateFailed, just re-raise it
                if isinstance(err, UpdateFailed):
                    raise err
                _LOGGER.error("Unexpected error: %s", err)
                raise MerakiConnectionError(f"Unexpected error: {err}") from err

        return cast(T, {})

    return cast(Callable[..., Coroutine[Any, Any, T]], wrapper)


def _is_rate_limit_error(err: APIError) -> bool:
    """Check if error is due to rate limiting."""
    return getattr(err, "status", None) == 429 or "rate limit" in str(err).lower()


def _is_auth_error(err: APIError) -> bool:
    """Check if error is an authentication error."""
    return getattr(err, "status", None) in (401, 403) or any(
        msg in str(err).lower()
        for msg in (
            "unauthorized",
            "forbidden",
            "invalid api key",
            "authentication failed",
        )
    )


def _is_device_error(err: APIError) -> bool:
    """Check if error is device-related."""
    return any(
        msg in str(err).lower()
        for msg in (
            "device not found",
            "invalid serial",
            "device error",
            "device offline",
        )
    )


def _is_network_error(err: APIError) -> bool:
    """Check if error is network-related."""
    return any(
        msg in str(err).lower()
        for msg in (
            "network not found",
            "invalid network",
            "network error",
            "network offline",
        )
    )


def _is_informational_error(err: APIError) -> bool:
    """Check if error is informational (e.g., feature not enabled)."""
    error_str = str(err).lower()
    return (
        "vlans are not enabled" in error_str
        or "traffic analysis" in error_str
        or "historical viewing is not supported" in error_str
    )


def validate_response(response: Any) -> Any:
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
