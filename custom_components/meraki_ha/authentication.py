"""Meraki API authentication functions for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha authentication.py loaded")  # Added Log


class MerakiAuthentication:
    """Class to handle Meraki API authentication."""

    def __init__(self, api_key: str, org_id: str):
        """Initialize the Meraki Authentication class."""
        self.api_key = api_key
        self.org_id = org_id

    async def validate_credentials(self) -> bool:
        """Validate Meraki API credentials.

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
            "X-Cisco-Meraki-API-Key": self.api_key,
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
                        if not any(org["id"] == self.org_id for org in organizations):
                            _LOGGER.error(f"Invalid Organization ID: {self.org_id}")
                            raise ValueError(f"Invalid Organization ID: {self.org_id}")
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


async def validate_meraki_credentials(api_key: str, org_id: str) -> bool:
    """Validate Meraki API credentials."""
    auth = MerakiAuthentication(api_key, org_id)
    return await auth.validate_credentials()
