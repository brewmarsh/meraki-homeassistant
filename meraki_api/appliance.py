# meraki_ha/meraki_api/appliance.py
import logging
import aiohttp
from .exceptions import MerakiApiError  # Import custom exception

_LOGGER = logging.getLogger(__name__)

async def get_meraki_device_appliance_uplinks(api_key, org_id, serial):
    """Fetch uplink settings for a Meraki MX appliance (async version)."""
    url = f"https://api.meraki.com/api/v1/devices/{serial}/appliance/uplinks/settings"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return await response.json()
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching uplink settings: {e}") from e