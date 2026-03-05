"""API exception handlers."""

import asyncio
import logging
from collections.abc import Callable
from typing import Any

from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError  # type: ignore

from ...errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
    MerakiDeviceError,
    MerakiInformationalError,
    MerakiNetworkError,
)
from .errors import (
    RetryRequest,
    is_auth_error,
    is_device_error,
    is_informational_error,
    is_network_error,
    is_rate_limit_error,
)
from .formatters import get_safe_return_value

_LOGGER = logging.getLogger(__name__)


def handle_invalid_response_error(func: Callable[..., Any], err: Exception) -> Any:
    """Handle empty or invalid responses."""
    _LOGGER.warning(
        "API call %s failed with an empty or invalid response: %s",
        func.__name__,
        err,
    )
    return get_safe_return_value(func)


def handle_feature_disabled(
    func: Callable[..., Any],
    err: Exception,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    """Handle disabled features by marking them in the client & returning safe value."""
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

    return get_safe_return_value(func, error_msg)


async def handle_rate_limit(
    err: APIError, attempt: int, max_retries: int, base_delay: int
) -> None:
    """Handle rate limiting by sleeping and raising RetryRequest."""
    if attempt >= max_retries:
        _LOGGER.warning(
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
    raise RetryRequest()


def handle_meraki_api_error(err: APIError) -> None:
    """Handle standard Meraki API errors."""
    _LOGGER.warning("Meraki API error: %s", err)
    if is_auth_error(err):
        raise MerakiAuthenticationError(f"Authentication failed: {err}") from err
    if is_device_error(err):
        raise MerakiDeviceError(f"Device error: {err}") from err
    if is_network_error(err):
        raise MerakiNetworkError(f"Network error: {err}") from err

    raise MerakiConnectionError(f"API error: {err}") from err


def handle_unexpected_error(err: Exception) -> None:
    """Handle unexpected exceptions."""
    if isinstance(err, UpdateFailed):
        raise err
    _LOGGER.warning("Unexpected error: %s", err)
    raise MerakiConnectionError(f"Unexpected error: {err}") from err


async def handle_api_exception(
    err: APIError | MerakiInformationalError,
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    retry_context: tuple[int, int, int],
) -> Any:
    """Handle APIError and MerakiInformationalError logic."""
    error_msg = str(err)

    # Check for disabled features
    if _is_feature_disabled_msg(error_msg):
        return handle_feature_disabled(func, err, args, kwargs)

    # Handle informational errors
    if isinstance(err, MerakiInformationalError):
        raise err
    if isinstance(err, APIError) and is_informational_error(err):
        raise MerakiInformationalError(f"Informational error: {err}") from err

    # Handle rate limits
    if isinstance(err, APIError) and is_rate_limit_error(err):
        attempt, max_retries, base_delay = retry_context
        await handle_rate_limit(err, attempt, max_retries, base_delay)

    # Handle other API errors
    if isinstance(err, APIError):
        handle_meraki_api_error(err)

    return None


def _is_feature_disabled_msg(error_msg: str) -> bool:
    """Check if error message indicates a disabled feature."""
    return (
        "Traffic Analysis with Hostname Visibility" in error_msg
        or "VLANs are not enabled for this network" in error_msg
    )
