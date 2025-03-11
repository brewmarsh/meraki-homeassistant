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
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    organizations = await response.json()
                    _LOGGER.debug(f"Organizations retrieved: {organizations}")
                    if not any(org["id"] == org_id for org in organizations):
                        _LOGGER.error(f"Invalid Organization ID: {org_id}")
                        raise ValueError(f"Invalid Organization ID: {org_id}")
                    _LOGGER.debug("Credentials validated successfully")
                    return True