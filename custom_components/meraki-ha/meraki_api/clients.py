# /config/custom_components/meraki_ha/meraki_api/clients.py
import logging
import aiohttp
import asyncio

_LOGGER = logging.getLogger(__name__)

async def get_clients(api_key, network_id):
    """Fetch connected clients from Meraki API."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                _LOGGER.debug(f"Meraki API raw text: {data}")
                return data
    except aiohttp.ClientError as err:
        _LOGGER.error(f"Error fetching Meraki clients: {err}")
        return []
    except Exception as err:
        _LOGGER.error(f"An unexpected error occurred: {err}")
        return []

async def update_connected_clients(api_key, network_id, device_list):
    """Update connected clients for all devices in the list."""
    for device in device_list:
        if device["model"].startswith("MR"):
            try:
                clients = await get_clients(api_key, network_id)
                device["connected_clients"] = len(clients)
            except Exception as err:
                _LOGGER.warning(f"Failed to fetch connected client count for {device['serial']}: {err}")