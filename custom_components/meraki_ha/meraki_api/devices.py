"""Handles Meraki device-specific API interactions.

This module provides functions to retrieve and manage information about
Meraki devices within an organization, including their clients and tags.
It utilizes the centralized `_async_meraki_request` for making API calls.
"""

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
    api_key: str, org_id: str
) -> Optional[List[Dict[str, Any]]]:
    """Retrieves all devices within a specified Meraki organization.

    This function fetches a list of all devices associated with the given
    organization ID. It processes the response to ensure that keys are not None
    and includes a small delay in the loop, which might be for rate limiting
    or yielding control in an async environment.

    Args:
        api_key (str): The Meraki API key for authentication.
        org_id (str): The ID of the Meraki organization.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries, where each
            dictionary represents a Meraki device. Returns None if an error
            occurs that prevents data retrieval, though current implementation
            raises MerakiApiError instead. The list can be empty if the
            organization has no devices.

    Raises:
        MerakiApiError: If an `aiohttp.ClientError` or any other exception
            occurs during the API request or data processing.
    """
    _LOGGER.debug("Retrieving Meraki devices for Org ID: %s", org_id)
    endpoint = f"/organizations/{org_id}/devices"
    try:
        # Fetch raw device data from the API.
        raw_devices_data = await _async_meraki_request(api_key, "GET", endpoint)
        _LOGGER.debug("Raw Meraki API response: %s", json.dumps(raw_devices_data))

        processed_devices: List[Dict[str, Any]] = []
        if isinstance(raw_devices_data, list): # Ensure the response is a list
            for device_info in raw_devices_data:
                _LOGGER.debug("Device before processing: %s", device_info)
                # Filter out entries where the key is None, though this is unusual for JSON.
                # It's more likely that a value could be None.
                # Assuming device_info is a dictionary.
                if isinstance(device_info, dict):
                    current_device_data = {
                        key: value for key, value in device_info.items() if key is not None
                    }
                    # Log if any key was None and thus skipped (which is rare for dict keys).
                    if len(current_device_data) != len(device_info):
                        _LOGGER.warning(
                            "Found and skipped None key in device data: %s", device_info
                        )
                    processed_devices.append(current_device_data)
                    _LOGGER.debug("Device after processing: %s", current_device_data)
                else:
                    _LOGGER.warning("Skipping non-dictionary item in device list: %s", device_info)
                # Consider if this sleep is strictly necessary or if it's a remnant.
                # If for rate limiting, it should be documented or handled more robustly.
                await asyncio.sleep(0.01) # Reduced sleep time, original was 1 second.
        else:
            _LOGGER.error("Received unexpected data format for devices: %s", raw_devices_data)
            # Depending on strictness, could return empty list or raise error.
            # For now, will result in empty list if not a list.
            # Consider raising MerakiApiError for unexpected format.

        return processed_devices
    except aiohttp.ClientError as e:
        _LOGGER.error("Aiohttp Client Error while retrieving devices: %s", e)
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        # Catching a broad exception can hide issues; consider more specific catches if possible.
        _LOGGER.error("General Error while retrieving devices: %s", e)
        raise MerakiApiError(f"General Error: {e}") from e


async def get_meraki_device_clients(
    api_key: str, network_id: str, serial: str
) -> List[Dict[str, Any]]:
    """Retrieves connected clients for a specific Meraki device.

    Note: The endpoint used is `/networks/{network_id}/clients`.
    This typically returns clients for a network. If the intention is clients
    for a *specific device*, the endpoint might need to be `/devices/{serial}/clients`.
    The current implementation fetches clients at the network level.
    The `serial` parameter is logged but not used in the API endpoint path.

    Args:
        api_key (str): The Meraki API key.
        network_id (str): The ID of the network to query for clients.
        serial (str): The serial number of the device (logged, but not used in API path).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a client.

    Raises:
        MerakiApiError: If an API error occurs.
    """
    # The endpoint implies fetching clients for the entire network, not just one device.
    # If device-specific clients are needed, the endpoint should be /devices/{serial}/clients.
    endpoint = f"/networks/{network_id}/clients"
    _LOGGER.debug(
        "Retrieving Meraki clients for network ID: %s (device serial: %s logged for context)",
        network_id,
        serial,
    )
    try:
        client_data = await _async_meraki_request(api_key, "GET", endpoint)
        _LOGGER.debug("Meraki API response for clients: %s", client_data)
        # Ensure data is a list, as expected.
        if not isinstance(client_data, list):
            _LOGGER.warning("Expected list of clients, got %s", type(client_data))
            return [] # Or raise an error if strict contract is required.
        return client_data
    except aiohttp.ClientError as e:
        _LOGGER.error("Error retrieving clients for network %s: %s", network_id, e)
        raise MerakiApiError(f"Error retrieving clients: {e}") from e
    except Exception as e:
        _LOGGER.error("Unexpected error retrieving clients for network %s: %s", network_id, e)
        raise MerakiApiError(f"Error retrieving clients: {e}") from e


async def get_device_tags(api_key: str, serial: str) -> List[str]:
    """Retrieves the tags for a specific Meraki device.

    Args:
        api_key (str): The Meraki API key.
        serial (str): The serial number of the device.

    Returns:
        List[str]: A list of tags associated with the device. Returns an
            empty list if the device has no tags or if a 404 error occurs
            (indicating the device might exist but has no tags endpoint or no tags).

    Raises:
        MerakiApiError: If any non-404 API error or other exception occurs.
    """
    endpoint = f"/devices/{serial}/tags"
    _LOGGER.debug("Retrieving tags for device serial: %s", serial)
    try:
        tag_data = await _async_meraki_request(api_key, "GET", endpoint)
        _LOGGER.debug("Meraki API response for tags: %s", tag_data)
        # The API is expected to return a list of strings.
        if not isinstance(tag_data, list) or not all(isinstance(tag, str) for tag in tag_data):
            _LOGGER.warning("Expected list of strings for tags, got %s", type(tag_data))
            # Decide on behavior: return empty list, or raise error.
            # Current code implies it expects list of strings from _async_meraki_request.
            return [] # Or raise MerakiApiError("Unexpected tag format")
        return tag_data
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            # A 404 could mean the device doesn't support tags or has no tags.
            # Returning an empty list is a common way to handle this.
            _LOGGER.warning(
                "Device tags not found (404) for device %s. Returning empty list.", serial
            )
            return []
        else:
            _LOGGER.error(
                "Failed to retrieve device tags for %s. Status: %s, Message: %s",
                serial,
                e.status,
                e.message,
            )
            raise MerakiApiError(
                f"Failed to retrieve device tags for {serial}. Status: {e.status}, Message: {e.message}"
            ) from e
    except aiohttp.ClientError as e:
        # Handles other client errors like connection issues.
        _LOGGER.error("Aiohttp Client Error retrieving tags for %s: %s", serial, e)
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error("Error retrieving device tags for %s: %s", serial, e)
        raise MerakiApiError(f"Error retrieving device tags: {e}") from e


async def update_device_tags(api_key: str, serial: str, tags: List[str]) -> bool:
    """Updates the tags for a specific Meraki device.

    This will replace all existing tags on the device with the new list of tags.

    Args:
        api_key (str): The Meraki API key.
        serial (str): The serial number of the device.
        tags (List[str]): A list of strings representing the desired tags.
            An empty list will remove all tags from the device.

    Returns:
        bool: True if the tags were updated successfully.

    Raises:
        MerakiApiError: If an API error occurs or if the update fails.
    """
    endpoint = f"/devices/{serial}/tags"
    _LOGGER.debug("Updating tags for device serial: %s with tags: %s", serial, tags)
    # The Meraki API expects a JSON payload with a "tags" key holding the list of strings.
    payload = {"tags": tags}
    try:
        # A successful PUT request to this endpoint usually returns the updated list of tags.
        response_data = await _async_meraki_request(
            api_key, "PUT", endpoint, data=payload
        )
        _LOGGER.debug("Device tags updated successfully. Response: %s", response_data)
        # Optionally, verify response_data matches the sent tags for stricter confirmation.
        return True
    except aiohttp.ClientError as e:
        _LOGGER.error("Aiohttp Client Error updating tags for %s: %s", serial, e)
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error("Error updating device tags for %s: %s", serial, e)
        raise MerakiApiError(f"Error updating device tags: {e}") from e
