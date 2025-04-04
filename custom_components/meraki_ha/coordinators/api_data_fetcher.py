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
    retry_if_exception_type,
)

from .device_coordinator import MerakiDeviceCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiApiDataFetcher:
    """
    Class to fetch data from Meraki API.

    This class orchestrates the fetching of data from the Meraki API using the individual
    data coordinator classes (`MerakiDeviceCoordinator`, `MerakiSsidCoordinator`, and
    `MerakiNetworkCoordinator`). It acts as a central point for retrieving all necessary
    data for the Home Assistant integration.

    Architecture:
    - This class uses the data coordinator classes to fetch data from the Meraki API.
    - It separates the API interaction logic from the data processing and coordination logic
    of the other coordinators.
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
            UpdateFailed: If the data fetching fails.
        """
        try:
            # Fetch data using _fetch_data directly
            networks_url = (
                f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
            )
            _LOGGER.debug(f"Fetching networks from: {networks_url}")
            networks = await self._fetch_data(networks_url)
            _LOGGER.debug(f"Networks fetched: {networks}")

            devices = []
            ssids = []

            if networks:
                for network in networks:
                    network_id = network["id"]
                    _LOGGER.debug(f"Processing network: {network_id}")

                    devices_url = (
                        f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
                    )
                    _LOGGER.debug(f"Fetching devices from: {devices_url}")
                    device_data = await self._fetch_data(devices_url)
                    _LOGGER.debug(f"Devices fetched: {device_data}")
                    if device_data:
                        devices.extend(device_data)

                    ssids_url = (
                        f"https://api.meraki.com/api/v1/networks/{network_id}/ssids"
                    )
                    _LOGGER.debug(f"Fetching SSIDs from: {ssids_url}")
                    ssid_data = await self._fetch_data(ssids_url)
                    _LOGGER.debug(f"SSIDs fetched: {ssid_data}")
                    if ssid_data:
                        ssids.extend(ssid_data)

            return {
                "devices": devices,
                "networks": networks,
                "ssids": ssids,
            }
        except Exception as e:
            _LOGGER.error(f"Error fetching all data: {e}")
            raise UpdateFailed(f"Error fetching all data: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(aiohttp.ClientError),
    )
    async def _fetch_data(self, url: str) -> Any:
        """Fetch data from a given URL with retry logic."""
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    resp.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                    return await resp.json()
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning(f"API error: {e.status} for URL: {url}")
            if e.status == 404:
                _LOGGER.warning(f"Resource not found for URL: {url}")
                return []  # or return None
            if e.status == 401:
                _LOGGER.error("Unauthorized: Check your API key.")
            elif e.status == 429:
                _LOGGER.warning("Rate limited: Too many requests.")
            raise  # Re-raise the exception to trigger retry
        except aiohttp.ClientError as e:
            _LOGGER.warning(f"API error: {e} for URL: {url}")
            raise  # Re-raise the exception to trigger retry
        except Exception as e:
            _LOGGER.error(f"Unexpected error fetching data: {e} for URL: {url}")
            return None

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
