# meraki_ha/meraki_api/authentication.py
import logging
import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)

async def validate_meraki_credentials(api_key, org_id):
    """Validate Meraki API credentials."""
    _LOGGER.debug("Validating Meraki credentials")
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        organizations = await response.json()
                        _LOGGER.debug(f"Organizations retrieved: {organizations}")
                        if not any(org["id"] == org_id for org in organizations):
                            _LOGGER.error(f"Invalid Organization ID: {org_id}")
                            raise ValueError(f"Invalid Organization ID: {org_id}")
                        _LOGGER.debug("Credentials validated successfully")
                        return True
                    elif response.status == 401:
                        _LOGGER.debug("Authentication failed (401)")
                        raise ConfigEntryAuthFailed
                    else:
                        _LOGGER.error(f"Meraki API Error: Status: {response.status}")
                        raise Exception(f"Meraki API Error: Status: {response.status}")
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Aiohttp Client Error: {e}")
                raise Exception(f"Aiohttp Client Error: {e}")
            except ConfigEntryAuthFailed:
                raise
            except ValueError as ve:
                _LOGGER.error(f"Value Error: {ve}")
                raise ve
            except Exception as e:
                _LOGGER.error(f"Error connecting to Meraki API: {e}")
                raise Exception(f"Error connecting to Meraki API: {e}")

    except Exception as e:
        _LOGGER.error(f"Outer Error: {e}")
        raise Exception(f"Outer Error: {e}")