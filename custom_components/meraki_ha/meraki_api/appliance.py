"""Meraki appliance API functions for the meraki_ha integration."""

import logging
from typing import Any, Dict

import aiohttp  # Keep the aiohttp import

from .exceptions import MerakiApiError
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)


async def get_meraki_device_appliance_uplinks(
    api_key: str, serial: str  # Removed session parameter
) -> Dict[str, Any]:
    """Fetch uplink settings for a Meraki MX appliance (async version).

    Args:
        api_key: Meraki API key. [cite: 1, 2]
        serial: Serial number of the Meraki MX appliance. [cite: 3, 4]

    Returns:
        A dictionary containing the uplink settings.

    Raises:
        MerakiApiError: If an error occurs during the API call. [cite: 17]
    """
    endpoint = f"/devices/{serial}/appliance/uplinks/settings"
    try:
        return await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching uplink settings: {e}") from e
    except Exception as e:
        _LOGGER.error(f"Unexpected error fetching uplink settings: {e}")
        raise MerakiApiError(f"Unexpected error fetching uplink settings: {e}") from e
