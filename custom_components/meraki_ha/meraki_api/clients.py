"""Handles Meraki client-specific API interactions.

This module provides functions to retrieve information about clients
connected to Meraki devices and includes a placeholder for updating
client information if such functionality is needed in the future.
It utilizes the centralized `_async_meraki_request` for API calls.
"""

import logging
from typing import Any, Dict, List

import aiohttp  # Keep the aiohttp import
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha clients.py loaded")  # Added Log


async def update_connected_clients(
    api_key: str,
    org_id: str,
    serial: str,
    clients: List[Dict[str, Any]],
) -> None:
    """Placeholder function for updating connected client information.

    Currently, this function serves as a placeholder and does not implement
    any actual client update logic. It logs a debug message indicating
    it has been called. This can be expanded in the future if the integration
    requires functionality to modify client settings or states via the API.

    Args:
        api_key (str): The Meraki API key. [cite: 1, 2]
        org_id (str): The Meraki organization ID.
        serial (str): The serial number of the Meraki device.
        clients (List[Dict[str, Any]]): A list of dictionaries, where each
            dictionary represents a client. This parameter is currently unused.
    """
    _LOGGER.debug(
        "Placeholder: update_connected_clients called for device serial: %s, org_id: %s",
        serial,
        org_id,
    )
    # Future client update logic would be implemented here.
    # For example, this could involve making POST or PUT requests
    # to specific client endpoints if the Meraki API supports such actions.
    # As of now, this function is non-operational for actual updates.


async def get_meraki_device_clients(
    api_key: str, serial: str
) -> List[Dict[str, Any]]:
    """Retrieves the list of clients connected to a specific Meraki device.

    This function queries the Meraki API to get details about all clients
    that are currently or were recently connected to the device identified
    by its serial number.

    Args:
        api_key (str): The Meraki API key for authentication.
        serial (str): The serial number of the Meraki device.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary
            contains information about a single client. The structure of these
            dictionaries is defined by the Meraki API. Common fields include
            'description', 'mac', 'ip', 'vlan', 'status', 'lastSeen', etc.
            Returns an empty list if no clients are found or if the device
            does not support client reporting.

    Raises:
        aiohttp.ClientError: If an HTTP-related error occurs during the API request
            (e.g., connection error, timeout).
        Exception: For any other unexpected errors encountered during the process.
            These are logged, and the original exception is re-raised.
    """
    endpoint = f"/devices/{serial}/clients"
    try:
        # Make the GET request to fetch client data.
        client_data = await _async_meraki_request(api_key, "GET", endpoint)
        return client_data
    except aiohttp.ClientError as e:
        # Log HTTP-specific errors.
        _LOGGER.error(
            "API_REQUEST_ERROR Error getting clients for device %s: %s", serial, e
        )
        raise  # Re-raise to allow for specific handling by the caller.
    except Exception as e:
        # Log any other unexpected errors.
        _LOGGER.error(
            "UNEXPECTED_ERROR Unexpected error getting clients for device %s: %s",
            serial,
            e,
        )
        raise  # Re-raise to ensure the error is not silently ignored.
