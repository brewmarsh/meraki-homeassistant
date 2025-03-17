# devices.py
"""Meraki device API functions for the meraki_ha integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
import json  # added import

import aiohttp
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha devices.py loaded")


async def get_meraki_devices(
    session: aiohttp.ClientSession, api_key: str, org_id: str
) -> Optional[List[Dict[str, Any]]]:
    """Retrieves all devices from a Meraki organization."""
    _LOGGER.debug(f"Retrieving Meraki devices for Org ID: {org_id}")
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices"
    try:
        _LOGGER.debug("Starting aiohttp session for device retrieval")
        try:
            _LOGGER.debug(f"Sending GET request to {url}")
            async with session.get(
                url, headers={"X-Cisco-Meraki-API-Key": api_key}
            ) as response:
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                raw_text = await response.text()
                _LOGGER.debug(f"Meraki API raw text: {raw_text}")
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.debug(
                        f"Raw Meraki API response: {json.dumps(data)}"
                    )  # added line
                    devices: List[Dict[str, Any]] = []
                    for device in data:
                        _LOGGER.debug(
                            f"Device before processing: {device}"
                        )  # added line
                        device_data = {}
                        for key, value in device.items():
                            if key is not None:
                                device_data[key] = value
                            else:
                                _LOGGER.warning(
                                    f"Found None key in device data: {device}"
                                )
                        devices.append(device_data)
                        _LOGGER.debug(
                            f"Device after processing: {device_data}"
                        )  # added line
                    await asyncio.sleep(1)
                    return devices
                else:
                    _LOGGER.error(
                        f"Meraki API Error during device retrieval: Status: {response.status}"
                    )
                    raise MerakiApiError(
                        f"Meraki API Error: Status: {response.status}, Text: {raw_text}"
                    )
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Aiohttp Client Error: {e}")
            raise MerakiApiError(f"Aiohttp Client Error: {e}")
        except Exception as e:
            _LOGGER.error(f"General Error: {e}")
            raise MerakiApiError(f"General Error: {e}")
    except Exception as e:
        _LOGGER.error(f"Outer Error: {e}")
        raise MerakiApiError(f"Outer Error: {e}")


async def get_meraki_device_clients(
    session: aiohttp.ClientSession, api_key: str, network_id: str, serial: str
) -> List[Dict[str, Any]]:
    """Retrieve connected clients for a specific Meraki device."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients"
    _LOGGER.debug(f"Retrieving Meraki clients for device serial: {serial}")
    try:
        _LOGGER.debug(f"Sending GET request to {url}")
        async with session.get(
            url, headers={"X-Cisco-Meraki-API-Key": api_key}
        ) as response:
            if response.status == 200:
                data = await response.json()
                _LOGGER.debug(f"Meraki API response status: {response.status}")
                _LOGGER.debug(f"Meraki API raw text: {data}")
                return data
            else:
                error_message = f"Failed to retrieve Meraki clients. Status: {response.status}, Text: {await response.text()}"
                _LOGGER.error(error_message)
                raise MerakiApiError(error_message)
    except Exception as e:
        _LOGGER.error(f"Error retrieving clients: {e}")
        raise MerakiApiError(f"Error retrieving clients: {e}")
