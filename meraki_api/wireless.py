# meraki_ha/meraki_api/wireless.py
import logging
import aiohttp
from .exceptions import MerakiApiError  # Import custom exception

_LOGGER = logging.getLogger(__name__)

async def get_meraki_device_wireless_radio_settings(api_key, org_id, serial):
    """Fetch wireless radio settings for a Meraki MR device (async version)."""
    url = f"https://api.meraki.com/api/v1/devices/{serial}/wireless/radio/settings"
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
        raise MerakiApiError(f"Error fetching wireless radio settings: {e}") from e

async def get_meraki_network_wireless_rf_profile(api_key, network_id, rf_profile_id):
    """Fetch wireless RF profile settings for a Meraki network (async version)."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/rfProfiles/{rf_profile_id}"
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
        raise MerakiApiError(f"Error fetching wireless RF profile settings: {e}") from e