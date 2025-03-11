"""Meraki appliance API functions for the meraki_ha integration."""
import logging
from typing import Any, Dict

import aiohttp

from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


async def get_meraki_device_appliance_uplinks(
    api_key: str, org_id: str, serial: str
) -> Dict[str, Any]:
    """Fetch uplink settings for a Meraki MX appliance (async version).

    Args:
        api_key: Meraki API key.
        org_id: Meraki organization ID.
        serial: Serial number of the Meraki MX appliance.

    Returns:
        A dictionary containing the uplink settings.

    Raises:
        MerakiApiError: If an error occurs during the API call.
    """
    url = f"https://api.meraki.com/api/v1/devices/{serial}/appliance/uplinks/settings"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching uplink settings: {e}") from e
    except Exception as e:
        _LOGGER.error(f"Unexpected error fetching uplink settings: {e}")
        raise MerakiApiError(f"Unexpected error fetching uplink settings: {e}") from e