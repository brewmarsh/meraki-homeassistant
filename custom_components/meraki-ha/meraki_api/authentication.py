"""Meraki API authentication functions for the meraki_ha integration."""
import logging
from typing import Any, List, Dict

import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha authentication.py loaded") #Added Log

async def validate_meraki_credentials(api_key: str, org_id: str) -> bool:
    """Validate Meraki API credentials.

    Args:
        api_key: Meraki API key.
        org_id: Meraki organization ID.

    Returns:
        True if credentials are valid.

    Raises:
        ConfigEntryAuthFailed: If authentication fails.
        ValueError: If the organization ID is invalid.
        Exception: For other API errors.
    """
    _LOGGER.debug("Validating Meraki credentials")
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        _LOGGER.debug("Starting aiohttp session for credential validation")
        async with aiohttp.ClientSession() as session:
            _LOGGER.debug(f"Sending GET request to {url}")
            async with session.get(url, headers=headers) as response:
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                if response.status == 200:
                    organizations: List[Dict[str, Any]] = await response.json()
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
    except ValueError as ve:
        _LOGGER.error(f"Value Error: {ve}")
        raise ve
    except ConfigEntryAuthFailed:
        raise
    except Exception as e:
        _LOGGER.error(f"Error connecting to Meraki API: {e}")
        raise Exception(f"Error connecting to Meraki API: {e}")