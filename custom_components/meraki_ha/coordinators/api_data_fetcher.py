"""API Data Fetcher for the meraki_ha integration."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
import aiohttp

_LOGGER = logging.getLogger(__name__)

MERAKI_API_URL = "https://api.meraki.com/api/v1"  # Define API URL as a constant


class MerakiApiError(Exception):
    """Base class for Meraki API exceptions."""

    pass


class MerakiApiConnectionError(Exception):
    """Exception raised for connection errors."""

    pass


class MerakiApiInvalidApiKeyError(Exception):
    """Exception raised for invalid API keys."""

    pass


class MerakiApiSsidFetchError(MerakiApiError):
    """Exception raised when fetching SSIDs fails."""

    pass


class MerakiApiDataFetcher:
    """
    Class to fetch data from Meraki API.
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        network_coordinator: Any,
        ssid_coordinator: Any,
    ):
        """
        Initialize the MerakiApiDataFetcher.
        """
        self.api_key = api_key
        self.org_id = org_id
        self.network_coordinator = network_coordinator
        self.ssid_coordinator = ssid_coordinator
        self.base_url = f"{MERAKI_API_URL}/organizations/{org_id}"

    async def fetch_all_data(
        self, hass: HomeAssistant, org_id: str, scan_interval, device_name_format: str
    ) -> Dict[str, Any]:  # Changed return type
        """
        Fetch all data from Meraki API.
        """
        networks = await self.async_get_networks(org_id)
        if networks is None:
            raise UpdateFailed("Could not fetch Meraki networks.")

        devices: List[Dict[str, Any]] = await self.async_get_organization_devices(
            org_id
        )
        if devices is None:
            raise UpdateFailed("Could not fetch Meraki devices.")

        ssids: List[Dict[str, Any]] = []
        network_clients: Dict[str, List[Dict[str, Any]]] = (
            {}
        )  # Store clients per network
        for network in networks:
            network_id = network["id"]
            try:
                ssid_data = await self.async_get_network_ssids(network_id)
                if ssid_data:
                    ssids.extend(ssid_data)
                clients_data = await self._fetch_data(
                    f"{MERAKI_API_URL}/networks/{network_id}/clients"
                )
                if clients_data:
                    network_clients[network_id] = clients_data
            except MerakiApiSsidFetchError:
                _LOGGER.warning(f"Could not fetch SSIDs for network {network_id}")
            except aiohttp.ClientResponseError as e:
                _LOGGER.warning(
                    f"API error fetching clients for network {network_id}: {e.status} - {e.message}"
                )
            except aiohttp.ClientError as e:
                _LOGGER.error(
                    f"Client error fetching clients for network {network_id}: {e}"
                )
            except Exception as e:
                _LOGGER.error(
                    f"Unexpected error fetching clients for network {network_id}: {e}"
                )

        # Restructure data to include connected clients in device info
        restructured_devices = []
        for device in devices:
            device_info = device.copy()
            if (
                "networkId" in device_info
                and device_info["networkId"] in network_clients
            ):
                connected_clients_count = sum(
                    1
                    for client in network_clients[device_info["networkId"]]
                    if client.get("recentDeviceSerial") == device_info["serial"]
                    and client.get("status") == "Online"
                )
                device_info["connected_clients"] = connected_clients_count
            else:
                device_info["connected_clients"] = 0
            restructured_devices.append(device_info)

        return {
            "devices": restructured_devices,
            "networks": networks,
            "ssids": ssids,
        }

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch networks for a Meraki organization."""
        url = f"{MERAKI_API_URL}/organizations/{org_id}/networks"
        _LOGGER.debug(f"Fetching networks from: {url}")
        return await self._fetch_data(url)

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get all devices in the Meraki organization.
        """
        url = f"{MERAKI_API_URL}/organizations/{org_id}/devices"
        _LOGGER.debug("Fetching devices from: %s", url)
        try:
            response = await self._fetch_data(url)
            return response
        except MerakiApiError as e:
            _LOGGER.warning("API error: %s for URL: %s", e, url)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error fetching devices: %s", e)
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch SSIDs from a Meraki network."""
        url = f"{MERAKI_API_URL}/networks/{network_id}/wireless/ssids"
        _LOGGER.debug(f"Fetching SSIDs from: {url}")
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning(f"API error: {e.status} - {e.message} for URL: {url}")
            if e.status == 404:
                _LOGGER.warning(f"Resource not found for URL: {url}")
                return []
            raise MerakiApiSsidFetchError(f"Failed to fetch SSIDs: {e}") from e
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Client error: {e} for URL: {url}")
            raise MerakiApiError(f"Client error occurred: {e}") from e
        except Exception as e:
            _LOGGER.error(f"Unexpected error fetching SSIDs: {e}")
            raise MerakiApiError(f"Unexpected error occurred: {e}") from e

    async def _fetch_data(self, url: str) -> Any:
        """Fetch data from a given URL."""
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Request headers: {headers}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single device."""
        # We might not need this anymore if tags are in the organization devices response.
        pass

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single device."""
        # We might not need this anymore if tags are in the organization devices response.
        pass
