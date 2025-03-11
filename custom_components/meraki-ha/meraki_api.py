# meraki_api.py
import logging
import aiohttp
import asyncio

from meraki.exceptions import APIError

from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)  # Create a logger instance


async def validate_meraki_credentials(api_key, org_id):
    """Validate Meraki API credentials."""
    _LOGGER.debug("Validating Meraki credentials")  # Add logging
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    organizations = await response.json()
                    _LOGGER.debug(f"Organizations retrieved: {organizations}")  # Log organizations

                    if not any(org["id"] == org_id for org in organizations):
                        _LOGGER.error(f"Invalid Organization ID: {org_id}")  # Log error, include org_id
                        raise ValueError(f"Invalid Organization ID: {org_id}")
                    _LOGGER.debug("Credentials validated successfully")
                    return True
                elif response.status == 401:
                    _LOGGER.debug("Authentication failed (401)")
                    raise ConfigEntryAuthFailed
                else:
                    _LOGGER.error(f"Meraki API Error: Status: {response.status}")
                    raise Exception(f"Meraki API Error: Status: {response.status}")
    except ValueError as ve:
        _LOGGER.error(f"Value Error: {ve}")
        raise ve
    except ConfigEntryAuthFailed:
        raise
    except Exception as e:
        _LOGGER.error(f"Error connecting to Meraki API: {e}")
        raise Exception(f"Error connecting to Meraki API: {e}")


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
                    _LOGGER.debug(f"Meraki API response status: {response.status}") #Log the status.
                    raw_text = await response.text()
                    _LOGGER.debug(f"Meraki API raw text: {raw_text}") # Log the raw text.
                    if response.status == 200:
                        devices = await response.json()
                        _LOGGER.debug(f"Retrieved {len(devices)} devices: {devices}")
                        await asyncio.sleep(1)  # Add rate limiting mitigation
                        return devices
                    else:
                        _LOGGER.error(f"Meraki API Error during device retrieval: Status: {response.status}")
                        return None #Return none so it doesn't cause a key error.
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Aiohttp Client Error: {e}")
                return None
            except Exception as e:
                _LOGGER.error(f"General Error: {e}")
                return None
    except Exception as e:
        _LOGGER.error(f"Outer Error: {e}")
        return None
    
class MerakiApiError(Exception):
    """Exception to indicate a Meraki API error."""
    pass

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

async def get_meraki_devices(api_key, org_id):
    """Fetch Meraki devices (async version)."""
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices"
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
        raise MerakiApiError(f"Error fetching Meraki devices: {e}") from e
