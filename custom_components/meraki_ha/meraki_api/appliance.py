"""Handles Meraki appliance-specific API interactions.

This module provides functions to retrieve information about Meraki
MX security appliances, such as their uplink settings. It utilizes the
centralized `_async_meraki_request` function for making API calls.
"""

import logging
from typing import Any, Dict

import aiohttp  # Keep the aiohttp import

from .exceptions import MerakiApiError
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)


async def get_meraki_device_appliance_uplinks(
    api_key: str, serial: str
) -> Dict[str, Any]:
    """Fetches uplink settings for a specific Meraki MX security appliance.

    This function retrieves the current uplink configuration and status for
    a given Meraki device identified by its serial number.

    Args:
        api_key (str): The Meraki API key for authentication. [cite: 1, 2]
        serial (str): The serial number of the Meraki MX appliance. [cite: 3, 4]

    Returns:
        Dict[str, Any]: A dictionary containing the uplink settings.
            The structure of this dictionary is defined by the Meraki API.
            Example:
            {
                "interfaces": [
                    {
                        "interface": "wan1",
                        "status": "active",
                        "ip": "1.2.3.4",
                        "gateway": "1.2.3.1",
                        "publicIp": "1.2.3.4",
                        "dns": ["8.8.8.8"],
                        "usingStaticIp": True
                    },
                    # ... other interfaces
                ]
            }

    Raises:
        MerakiApiError: If an error occurs during the API call, such as
            a connection issue, an invalid API key, or if the specified
            device is not found or not an MX appliance. [cite: 17]
    """
    endpoint = f"/devices/{serial}/appliance/uplinks/settings"
    try:
        # Make the GET request to the Meraki API.
        response_data = await _async_meraki_request(api_key, "GET", endpoint)
        return response_data
    except aiohttp.ClientError as e:
        # Handle errors specific to the HTTP request (e.g., connection, timeout).
        _LOGGER.error(
            "API_REQUEST_ERROR Error fetching uplink settings for device %s: %s",
            serial,
            e,
        )
        raise MerakiApiError(
            f"Error fetching uplink settings for device {serial}: {e}"
        ) from e
    except Exception as e:
        # Handle any other unexpected errors.
        _LOGGER.error(
            "UNEXPECTED_ERROR Unexpected error fetching uplink settings for device %s: %s",
            serial,
            e,
        )
        raise MerakiApiError(
            f"Unexpected error fetching uplink settings for device {serial}: {e}"
        ) from e
