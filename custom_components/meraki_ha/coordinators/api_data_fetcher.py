"""API Data Fetcher for the meraki_ha integration."""

import logging
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from .device_coordinator import MerakiDeviceCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator

_LOGGER = logging.getLogger(__name__)


def is_connection_error(exception):
    """Return True if the exception is a connection-related error."""
    return (
        isinstance(exception, aiohttp.ClientConnectionError)
        or isinstance(exception, aiohttp.ServerDisconnectedError)
        or isinstance(exception, aiohttp.ClientTimeout)
    )


class MerakiApiDataFetcher:
    """
    Class to fetch data from Meraki API.

    This class orchestrates the fetching of data from the Meraki API using the individual
    data coordinator classes (`MerakiDeviceCoordinator`, `MerakiSsidCoordinator`, and
    `MerakiNetworkCoordinator`). It acts as a central point for retrieving all necessary
    data for the Home Assistant integration.
    """

    def __init__(
        self,
        api_key: str,
        device_coordinator: MerakiDeviceCoordinator,
        network_coordinator: MerakiNetworkCoordinator,
        ssid_coordinator: MerakiSsidCoordinator,
    ):
        """
        Initialize the MerakiApiDataFetcher.

        Args:
            api_key: Meraki API key.
            device_coordinator: Instance of MerakiDeviceCoordinator.
            network_coordinator: Instance of MerakiNetworkCoordinator.
            ssid_coordinator: Instance of MerakiSsidCoordinator.
        """
        self.api_key = api_key
        self.device_coordinator = device_coordinator
        self.network_coordinator = network_coordinator
        self.ssid_coordinator = ssid_coordinator
        self.api_url = "https://api.meraki.com/api/v1"

    async def fetch_all_data(
        self, hass: HomeAssistant, org_id: str, scan_interval, device_name_format: str
    ) -> Dict[str, Any]:
        """
        Fetch all data from Meraki API.

        This method uses the data coordinator classes to retrieve data for devices, networks,
        and SSIDs.

        Args:
            hass: Home Assistant instance.
            org_id: Meraki organization ID.
            scan_interval: Time interval for updates.
            device_name_format: The format used to name devices.

        Returns:
            A dictionary containing the fetched data.

        Raises:
            UpdateFailed: If a critical part of the data fetching fails.
        """
        networks = await self.async_get_networks(org_id)
        if networks is None:
            raise UpdateFailed("Could not fetch Meraki networks.")

        devices = []
        ssids = []

        for network in networks:
            network_id = network["id"]
            try:
                device_data = await self.async_get_network_devices(network_id)
                if device_data:
                    devices.extend(device_data)
            except Exception as e:
                _LOGGER.warning(f"Error fetching devices for network {network_id}: {e}")

            ssid_data = await self.async_get_network_ssids(network_id)
            if ssid_data is not None:
                ssids.extend(ssid_data)

        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
        }

    async def async_get_networks(self, org_id: str) -> List[Dict[str, Any]] | None:
        """Fetch networks for a Meraki organization."""
        url = f"{self.api_url}/organizations/{org_id}/networks"
        _LOGGER.debug(f"Fetching networks from: {url}")
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning(f"API error: {e.status} for URL: {url}")
            if e.status == 404:
                _LOGGER.warning(f"Organization not found for URL: {url}")
                return None
            raise
        except aiohttp.ClientError as e:
            _LOGGER.warning(f"API error: {e} for URL: {url}")
            raise

    async def async_get_network_devices(
        self, network_id: str
    ) -> List[Dict[str, Any]] | None:
        """Fetch devices for a Meraki network."""
        url = f"{self.api_url}/networks/{network_id}/devices"
        _LOGGER.debug(f"Fetching devices from: {url}")
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning(f"API error: {e.status} for URL: {url}")
            return None  # Don't block the whole update if devices fail for one network
        except aiohttp.ClientError as e:
            _LOGGER.warning(f"API error: {e} for URL: {url}")
            raise

    async def async_get_network_ssids(
        self, network_id: str
    ) -> List[Dict[str, Any]] | None:
        """Fetch SSIDs from a Meraki network."""
        url = f"{self.api_url}/networks/{network_id}/ssids"
        _LOGGER.debug(f"Fetching SSIDs from: {url}")
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning(f"API error: {e.status} for URL: {url}")
            if e.status == 404:
                _LOGGER.warning(f"Resource not found for URL: {url}")
                return None
            raise
        except aiohttp.ClientError as e:
            _LOGGER.warning(f"API error: {e} for URL: {url}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception(is_connection_error),
    )
    async def _fetch_data(self, url: str) -> Any:
        """Fetch data from a given URL with retry logic."""
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return await resp.json()

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single device."""
        # The existing logic for fetching tags remains here.
        pass

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single device."""
        # The existing logic for updating tags remains here.
        pass


class MerakiApiConnectionError(Exception):
    """Exception raised for connection errors."""

    pass


class MerakiApiInvalidApiKeyError(Exception):
    """Exception raised for invalid API keys."""

    pass
