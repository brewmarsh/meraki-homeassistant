"""Meraki device API functions for the meraki_ha integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha devices.py loaded")  # Added Log


async def get_meraki_devices(
    api_key: str, org_id: str
) -> Optional[List[Dict[str, Any]]]:
    """Retrieves all devices from a Meraki organization.

    Args:
        api_key: Meraki API key.
        org_id: Meraki organization ID.

    Returns:
        A list of dictionaries representing Meraki devices, or None if an error occurs.
    """
    _LOGGER.debug(f"Retrieving Meraki devices for Org ID: {org_id}")
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        _LOGGER.debug("Starting aiohttp session for device retrieval")
        async with aiohttp.ClientSession() as session:
            try:
                _LOGGER.debug(f"Sending GET request to {url}")
                async with session.get(url, headers=headers) as response:
                    _LOGGER.debug(f"Meraki API response status: {response.status}")
                    raw_text = await response.text()
                    _LOGGER.debug(f"Meraki API raw text: {raw_text}")
                    if response.status == 200:
                        devices: List[Dict[str, Any]] = await response.json()
                        _LOGGER.debug(f"Retrieved {len(devices)} devices: {devices}")
                        await asyncio.sleep(1)  # Add rate limiting mitigation
                        return devices
                    else:
                        _LOGGER.error(
                            f"Meraki API Error during device retrieval: Status: {response.status}"
                        )
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
