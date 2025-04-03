"""Meraki wireless API functions for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

import aiohttp  # Keep aiohttp import

from .exceptions import MerakiApiError
from ._api_client import _async_meraki_request  # Import the common function

_LOGGER = logging.getLogger(__name__)


async def get_meraki_device_wireless_radio_settings(
    api_key: str, serial: str  # Removed session parameter
) -> Dict[str, Any]:
    """Fetch wireless radio settings for a Meraki MR device (async version)."""
    endpoint = f"/devices/{serial}/wireless/radio/settings"
    try:
        return await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching wireless radio settings: {e}") from e


async def get_meraki_network_wireless_rf_profile(
    api_key: str, network_id: str, rf_profile_id: str  # Removed session parameter
) -> Dict[str, Any]:
    """Fetch wireless RF profile settings for a Meraki network (async version)."""
    endpoint = f"/networks/{network_id}/wireless/rfProfiles/{rf_profile_id}"
    try:
        return await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching wireless RF profile settings: {e}") from e


async def get_meraki_connected_client_count(
    api_key: str, network_id: str, ap_mac: str  # Removed session parameter
) -> int:
    """Gets the count of clients connected to a specific Meraki access point."""
    endpoint = f"/networks/{network_id}/clients"
    try:
        clients: List[Dict[str, Any]] = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        connected_clients = [
            client
            for client in clients
            if client.get("apMac") == ap_mac and client.get("status") == "Online"
        ]
        return len(connected_clients)
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching connected client count: {e}") from e


async def get_meraki_ssids(
    api_key: str, network_id: str  # Removed session parameter
) -> List[Dict[str, Any]]:
    """Get the SSIDs for the network."""
    endpoint = f"/networks/{network_id}/wireless/ssids"
    _LOGGER.debug(f"get_meraki_ssids: Sending GET request to {endpoint}")
    try:
        ssids = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        _LOGGER.debug(f"get_meraki_ssids: Meraki API response: {ssids}")
        return ssids
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching network SSIDs: {e}") from e
