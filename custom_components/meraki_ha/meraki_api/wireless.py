"""Meraki wireless API functions for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

import aiohttp

from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


async def get_meraki_device_wireless_radio_settings(
    api_key: str, org_id: str, serial: str
) -> Dict[str, Any]:
    """Fetch wireless radio settings for a Meraki MR device (async version)."""
    url = f"https://api.meraki.com/api/v1/devices/{serial}/wireless/radio/settings"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching wireless radio settings: {e}") from e


async def get_meraki_network_wireless_rf_profile(
    api_key: str, network_id: str, rf_profile_id: str
) -> Dict[str, Any]:
    """Fetch wireless RF profile settings for a Meraki network (async version)."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/rfProfiles/{rf_profile_id}"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching wireless RF profile settings: {e}") from e


async def get_meraki_connected_client_count(
    api_key: str, network_id: str, ap_mac: str
) -> int:
    """Gets the count of clients connected to a specific Meraki access point."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                clients: List[Dict[str, Any]] = await response.json()
                connected_clients = [
                    client
                    for client in clients
                    if client.get("apMac") == ap_mac
                    and client.get("status") == "Online"
                ]
                return len(connected_clients)
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching connected client count: {e}") from e


async def get_meraki_network_ssids(
    api_key: str, network_id: str, session: aiohttp.ClientSession
) -> List[Dict[str, Any]]:
    """Get the SSIDs for the network."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/ssids"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    _LOGGER.debug(f"get_meraki_network_ssids: Sending GET request to {url}")
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            ssids = await response.json()
            _LOGGER.debug(f"get_meraki_network_ssids: Meraki API response: {ssids}")
            return ssids
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching network SSIDs: {e}") from e


async def get_meraki_network_ssid_schedule(
    api_key: str, network_id: str, ssid_number: int, session: aiohttp.ClientSession
) -> bool:
    """Get the schedule for an SSID."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/ssids/{ssid_number}"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            ssid_data = await response.json()
            if ssid_data and "availability" in ssid_data:
                return ssid_data["availability"]["enabled"]
            return None
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching SSID schedule: {e}") from e


async def update_meraki_network_ssid_schedule(
    api_key: str,
    network_id: str,
    ssid_number: int,
    enabled: bool,
    session: aiohttp.ClientSession,
) -> Dict[str, Any]:
    """Enable or disable the schedule for an SSID."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/ssids/{ssid_number}"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    data = {"availability": {"enabled": enabled}}
    try:
        async with session.put(url, headers=headers, json=data) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error updating SSID schedule: {e}") from e


async def get_meraki_ssids(
    network_id: str, api_key: str, session: aiohttp.ClientSession
) -> List[Dict[str, Any]]:
    """Get the SSIDs for the network."""
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }
    _LOGGER.debug(f"get_meraki_ssids: Sending GET request to {url}")
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            ssids = await response.json()
            _LOGGER.debug(f"get_meraki_ssids: Meraki API response: {ssids}")
            return ssids
    except aiohttp.ClientError as e:
        raise MerakiApiError(f"Error fetching network SSIDs: {e}") from e
