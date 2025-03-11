"""Meraki client API functions for the meraki_ha integration."""
import logging
from typing import Any, Dict, List

import aiohttp

_LOGGER = logging.getLogger(__name__)


async def get_clients(api_key: str, network_id: str) -> List[Dict[str, Any]]:
    """Fetch connected clients from Meraki API.

    Args:
        api_key: Meraki API key.
        network_id: Meraki network ID.

    Returns:
        A list of dictionaries representing connected clients.
    """
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data: List[Dict[str, Any]] = await response.json()
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                _LOGGER.debug(f"Meraki API raw text: {data}")
                return data
    except aiohttp.ClientError as err:
        _LOGGER.error(f"Error fetching Meraki clients: {err}")
        return []
    except Exception as err:
        _LOGGER.error(f"An unexpected error occurred: {err}")
        return []


async def update_connected_clients(
    api_key: str, network_id: str, device_list: List[Dict[str, Any]]
) -> None:
    """Update connected clients for all devices in the list.

    Args:
        api_key: Meraki API key.
        network_id: Meraki network ID.
        device_list: List of device dictionaries.
    """
    for device in device_list:
        if device["model"].startswith("MR"):
            try:
                clients: List[Dict[str, Any]] = await get_clients(api_key, network_id)
                device["connected_clients"] = len(clients)
            except Exception as err:
                _LOGGER.warning(
                    f"Failed to fetch connected client count for {device['serial']}: {err}"
                )