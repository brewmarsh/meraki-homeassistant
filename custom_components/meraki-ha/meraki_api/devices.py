# meraki_ha/meraki_api/devices.py
import logging
import aiohttp
import asyncio
from .exceptions import MerakiApiError  # Import custom exception

_LOGGER = logging.getLogger(__name__)

async def get_meraki_devices(api_key, org_id):
    """Retrieves all devices from a Meraki organization."""
    _LOGGER.debug(f"Retrieving Meraki devices for Org ID: {org_id}")
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    _LOGGER.debug(f"Meraki API response status: {response.status}")
                    raw_text = await response.text()
                    _LOGGER.debug(f"Meraki API raw text: {raw_text}")
                    if response.status == 200:
                        devices = await response.json()
                        _LOGGER.debug(f"Retrieved {len(devices)} devices: {devices}")
                        await asyncio.sleep(1)  # Add rate limiting mitigation
                        return devices
                    else:
                        _LOGGER.error(f"Meraki API Error during device retrieval: Status: {response.status}")
                        return None  # Return None to avoid KeyError
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Aiohttp Client Error: {e}")
                return None
            except Exception as e:
                _LOGGER.error(f"General Error: {e}")
                return None
    except Exception as e:
        _LOGGER.error(f"Outer Error: {e}")
        return None