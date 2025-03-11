"""Meraki client API functions for the meraki_ha integration."""
import logging
from typing import Any, Dict, List

import aiohttp

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha clients.py loaded") #Added Log

async def get_clients(api_key: str, network_id: str, serial_number: str = None) -> List[Dict[str, Any]]:
    """Fetch connected clients from Meraki API.

    Args:
        api_key: Meraki API key.
        network_id: Meraki network ID.
        serial_number: (Optional) Meraki device serial number.

    Returns:
        A list of dictionaries representing connected clients.
    """
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        _LOGGER.debug(f"Starting aiohttp session for clients retrieval")
        async with aiohttp.ClientSession() as session:
            _LOGGER.debug(f"Sending GET request to {url}")
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data: List[Dict[str, Any]] = await response.json()
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                _LOGGER.debug(f"Meraki API raw text: {data}")

                if serial_number:
                    # Filter clients based on the serial number (if needed)
                    filtered_clients = [client for client in data if client.get("deviceSerial") == serial_number]
                    _LOGGER.debug(f"Filtered clients by serial number: {filtered_clients}")
                    return filtered_clients
                else:
                    _LOGGER.debug(f"Returning all clients: {data}")
                    return data
    except aiohttp.ClientError as err:
        _LOGGER.error(f"Error fetching Meraki clients: {err}")
        _LOGGER.debug(f"Returning empty list due to aiohttp Client Error")
        return []
    except Exception as err:
        _LOGGER.error(f"An unexpected error occurred: {err}")
        _LOGGER.debug(f"Returning empty list due to unexpected error")
        return []