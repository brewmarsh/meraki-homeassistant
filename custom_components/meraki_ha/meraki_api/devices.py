#   devices.py
"""Meraki device API functions for the meraki_ha integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
import json  #   added import

import aiohttp  # Keep aiohttp import
from .exceptions import MerakiApiError
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha devices.py loaded")


async def get_meraki_devices(
    api_key: str, org_id: str  # Removed session parameter
) -> Optional[List[Dict[str, Any]]]:
    """Retrieves all devices from a Meraki organization."""

    _LOGGER.debug(f"Retrieving Meraki devices for Org ID: {org_id}")
    endpoint = f"/organizations/{org_id}/devices"
    try:
        data = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        _LOGGER.debug(f"Raw Meraki API response: {json.dumps(data)}")  #   added line
        devices: List[Dict[str, Any]] = []
        for device in data:
            _LOGGER.debug(f"Device before processing: {device}")  #   added line
            device_data = {}
            for key, value in device.items():
                if key is not None:
                    device_data[key] = value
                else:
                    _LOGGER.warning(f"Found None key in device data: {device}")
            devices.append(device_data)
            _LOGGER.debug(f"Device after processing: {device_data}")  #   added line
            await asyncio.sleep(1)
        return devices
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Aiohttp Client Error: {e}")
        raise MerakiApiError(f"Aiohttp Client Error: {e}")
    except Exception as e:
        _LOGGER.error(f"General Error: {e}")
        raise MerakiApiError(f"General Error: {e}")


async def get_meraki_device_clients(
    api_key: str, network_id: str, serial: str  # Removed session parameter
) -> List[Dict[str, Any]]:
    """Retrieve connected clients for a specific Meraki device."""

    endpoint = f"/networks/{network_id}/clients"
    _LOGGER.debug(f"Retrieving Meraki clients for device serial: {serial}")
    try:
        data = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        _LOGGER.debug(f"Meraki API response: {data}")
        return data
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error retrieving clients: {e}")
        raise MerakiApiError(f"Error retrieving clients: {e}")
    except Exception as e:
        _LOGGER.error(f"Error retrieving clients: {e}")
        raise MerakiApiError(f"Error retrieving clients: {e}")


async def get_device_tags(
    api_key: str, serial: str  # Removed session parameter
) -> Optional[List[str]]:
    """Retrieves the tags for a specific Meraki device."""

    endpoint = f"/devices/{serial}/tags"
    _LOGGER.debug(f"Retrieving tags for device serial: {serial}")
    try:
        data = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        _LOGGER.debug(f"Meraki API response: {data}")
        return data  #   Assuming the API returns a list of tag strings
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            _LOGGER.warning(f"Device tags not found for device {serial}.")
            return []  #   Return an empty list for 404 errors
        else:
            _LOGGER.error(
                f"Failed to retrieve device tags for device {serial}. Status: {e.status}, Text: {e.message}"
            )
            raise MerakiApiError(
                f"Failed to retrieve device tags for device {serial}. Status: {e.status}, Text: {e.message}"
            )
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Aiohttp Client Error: {e}")
        raise MerakiApiError(f"Aiohttp Client Error: {e}")
    except Exception as e:
        _LOGGER.error(f"Error retrieving device tags: {e}")
        raise MerakiApiError(f"Error retrieving device tags: {e}")


async def update_device_tags(
    api_key: str, serial: str, tags: List[str]  # Removed session parameter
) -> bool:
    """Updates the tags for a specific Meraki device."""

    endpoint = f"/devices/{serial}/tags"
    _LOGGER.debug(f"Updating tags for device serial: {serial} with tags: {tags}")
    payload = {"tags": tags}
    try:
        await _async_meraki_request(
            api_key, "PUT", endpoint, data=payload
        )  #   Use _async_meraki_request for PUT # Removed session argument
        _LOGGER.debug("Device tags updated successfully")
        return True
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Aiohttp Client Error: {e}")
        raise MerakiApiError(f"Aiohttp Client Error: {e}")
    except Exception as e:
        _LOGGER.error(f"Error updating device tags: {e}")
        raise MerakiApiError(f"Error updating device tags: {e}")
