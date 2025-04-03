"""Meraki client API functions for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

import aiohttp  # Keep the aiohttp import
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha clients.py loaded")  # Added Log


async def update_connected_clients(
    api_key: str,  # Removed session parameter
    org_id: str,
    serial: str,
    clients: List[Dict[str, Any]],
) -> None:
    """Update connected clients (currently a placeholder).

    This function is a placeholder and doesn't perform any actual updates.
    It can be expanded to implement client update logic if needed.

    Args:
        api_key: Meraki API key. [cite: 1, 2]
        org_id: Meraki organization ID.
        serial: Meraki device serial number.
        clients: List of connected clients (currently unused).
    """
    _LOGGER.debug(f"Updating connected clients for device serial: {serial}")
    # Add your client update logic here if required.
    # For now, it's just a placeholder.
    _LOGGER.debug(f"Client update placeholder called for {serial}")


async def get_meraki_device_clients(
    api_key: str, serial: str  # Removed session parameter
) -> List[Dict[str, Any]]:
    """
    Get the clients associated with a device

     Args:
        api_key: Meraki API key
        serial: device serial number

    Returns:
        A list of clients associated with the device.
    """

    endpoint = f"/devices/{serial}/clients"
    try:
        return await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error getting clients for device {serial}: {e}")
        raise
    except Exception as e:
        _LOGGER.error(f"Unexpected error getting clients for device {serial}: {e}")
        raise
