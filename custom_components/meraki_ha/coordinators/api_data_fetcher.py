"""Provides a centralized data fetcher for the Meraki Home Assistant integration.

This module defines `MerakiApiDataFetcher`, a class responsible for making
API calls to the Meraki dashboard to retrieve network, device, and SSID
information. It incorporates retry logic for transient network issues and
standardizes the fetching process. It also defines custom exceptions for
API-related errors.
"""

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


def is_connection_error(exception: Exception) -> bool:
    """Determines if an exception is a common transient connection error.

    This helper function is used by `tenacity.retry` to decide whether
    an API call should be retried.

    Args:
        exception (Exception): The exception instance to check.

    Returns:
        bool: True if the exception is an instance of `aiohttp.ClientConnectionError`,
              `aiohttp.ServerDisconnectedError`, or `aiohttp.ClientTimeout`.
              False otherwise.
    """
    return isinstance(
        exception,
        (
            aiohttp.ClientConnectionError,
            aiohttp.ServerDisconnectedError,
            aiohttp.ClientTimeout,
        ),
    )


class MerakiApiDataFetcher:
    """Fetches and coordinates data from various Meraki API endpoints.

    This class is responsible for making HTTP GET requests to the Meraki API
    to retrieve information about networks, devices, and SSIDs. It uses
    instances of other coordinators (though not directly in its current methods,
    it's structured to potentially delegate to them or be used by a higher-level
    coordinator). It includes retry mechanisms for robust data fetching.

    Attributes:
        api_key (str): The Meraki API key used for authentication.
        device_coordinator (MerakiDeviceCoordinator): Coordinator for device-specific data.
            (Note: Currently passed in __init__ but not directly used by methods in this class).
        network_coordinator (MerakiNetworkCoordinator): Coordinator for network-specific data.
            (Note: Currently passed in __init__ but not directly used by methods in this class).
        ssid_coordinator (MerakiSsidCoordinator): Coordinator for SSID-specific data.
            (Note: Currently passed in __init__ but not directly used by methods in this class).
        api_url (str): The base URL for the Meraki API (v1).
    """

    def __init__(
        self,
        api_key: str,
        device_coordinator: MerakiDeviceCoordinator,
        network_coordinator: MerakiNetworkCoordinator,
        ssid_coordinator: MerakiSsidCoordinator,
    ) -> None:
        """Initializes the MerakiApiDataFetcher.

        Args:
            api_key (str): The Meraki API key.
            device_coordinator (MerakiDeviceCoordinator): An instance of
                `MerakiDeviceCoordinator`.
            network_coordinator (MerakiNetworkCoordinator): An instance of
                `MerakiNetworkCoordinator`.
            ssid_coordinator (MerakiSsidCoordinator): An instance of
                `MerakiSsidCoordinator`.
        """
        self.api_key = api_key
        # These coordinators are stored but not directly used by the fetch_all_data
        # or other _fetch_data methods in this specific class. They might be intended
        # for future use or for interaction at a higher level of coordination.
        self.device_coordinator = device_coordinator
        self.network_coordinator = network_coordinator
        self.ssid_coordinator = ssid_coordinator
        self.api_url = "https://api.meraki.com/api/v1"

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        org_id: str,
        scan_interval,  # pylint: disable=unused-argument
        device_name_format: str,  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        """Fetches all required data (networks, devices, SSIDs) from the Meraki API.

        This method orchestrates calls to retrieve network information, then
        iterates through each network to get its associated devices and SSIDs.

        Args:
            hass (HomeAssistant): The Home Assistant instance. Currently unused.
            org_id (str): The Meraki organization ID.
            scan_interval: The scan interval for updates. Currently unused.
            device_name_format (str): The format for device names. Currently unused.

        Returns:
            Dict[str, Any]: A dictionary containing lists of 'devices',
                'networks', and 'ssids'.

        Raises:
            UpdateFailed: If the initial fetching of Meraki networks fails, as this
                is considered a critical step for further data retrieval.
        """
        networks = await self.async_get_networks(org_id)
        if networks is None:  # This condition implies async_get_networks can return None
            _LOGGER.error(
                "Failed to fetch Meraki networks for organization ID: %s. Cannot proceed.",
                org_id,
            )
            raise UpdateFailed("Could not fetch Meraki networks.")

        devices: List[Dict[str, Any]] = []
        ssids: List[Dict[str, Any]] = []

        # Iterate over each network to fetch its devices and SSIDs
        for network in networks:
            network_id = network.get("id")
            if not network_id:
                _LOGGER.warning("Network found without an ID: %s", network)
                continue  # Skip this network if it has no ID

            try:
                # Fetch devices for the current network
                device_data = await self.async_get_network_devices(network_id)
                if device_data:  # device_data can be None if fetching fails
                    devices.extend(device_data)
            except Exception as e:  # Catch broad exceptions during device fetch for a single network
                _LOGGER.warning(
                    "Error fetching devices for network %s: %s. Continuing with other networks.",
                    network_id,
                    e,
                )

            # Fetch SSIDs for the current network
            ssid_data = await self.async_get_network_ssids(network_id)
            if ssid_data is not None:  # ssid_data can be None
                ssids.extend(ssid_data)

        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
        }

    async def async_get_networks(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetches all networks for a given Meraki organization ID.

        Args:
            org_id (str): The Meraki organization ID.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of network dictionaries if
                successful, or None if a 404 error (Organization Not Found) occurs.

        Raises:
            aiohttp.ClientResponseError: For API errors other than 404.
            aiohttp.ClientError: For client-side connection issues.
        """
        url = f"{self.api_url}/organizations/{org_id}/networks"
        _LOGGER.debug("Fetching networks from: %s", url)
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning("API response error: %s for URL: %s", e.status, url)
            if e.status == 404:  # Specifically handle Organization Not Found
                _LOGGER.warning("Organization %s not found (404) at URL: %s", org_id, url)
                return None  # Return None for 404, allowing graceful handling
            raise  # Re-raise other response errors
        except aiohttp.ClientError as e:
            # Log other client errors (connection, timeout, etc.)
            _LOGGER.warning("Client API error: %s for URL: %s", e, url)
            raise  # Re-raise client errors

    async def async_get_network_devices(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetches all devices for a given Meraki network ID.

        Args:
            network_id (str): The Meraki network ID.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of device dictionaries if
                successful, or None if an API response error occurs (e.g., 404).
                This prevents failure for one network from halting all updates.

        Raises:
            aiohttp.ClientError: For client-side connection issues.
        """
        url = f"{self.api_url}/networks/{network_id}/devices"
        _LOGGER.debug("Fetching devices from: %s", url)
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            # Log and return None to prevent one network's failure from stopping all.
            _LOGGER.warning(
                "API response error: %s for devices at URL: %s. Returning None for this network's devices.",
                e.status,
                url,
            )
            return None
        except aiohttp.ClientError as e:
            _LOGGER.warning("Client API error: %s for URL: %s", e, url)
            raise  # Re-raise client errors as they might indicate broader issues

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetches all SSIDs for a given Meraki network ID.

        Args:
            network_id (str): The Meraki network ID.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of SSID dictionaries if
                successful, or None if a 404 error (Resource Not Found) occurs.

        Raises:
            aiohttp.ClientResponseError: For API errors other than 404.
            aiohttp.ClientError: For client-side connection issues.
        """
        url = f"{self.api_url}/networks/{network_id}/ssids"
        _LOGGER.debug("Fetching SSIDs from: %s", url)
        try:
            return await self._fetch_data(url)
        except aiohttp.ClientResponseError as e:
            _LOGGER.warning("API response error: %s for SSIDs at URL: %s", e.status, url)
            if e.status == 404:  # Handle SSID list not found for a network
                _LOGGER.warning("SSID resource not found (404) for network %s at URL: %s", network_id, url)
                return None
            raise  # Re-raise other response errors
        except aiohttp.ClientError as e:
            _LOGGER.warning("Client API error: %s for URL: %s", e, url)
            raise  # Re-raise client errors

    @retry(
        stop=stop_after_attempt(3),  # Retry up to 3 times
        wait=wait_exponential(multiplier=1, min=4, max=10),  # Exponential backoff
        retry=retry_if_exception(is_connection_error),  # Custom retry condition
    )
    async def _fetch_data(self, url: str) -> Any:
        """Performs an HTTP GET request to the given URL with retry logic.

        This is a general-purpose fetch method used by the more specific
        `async_get_*` methods. It includes the API key in headers and handles
        raising exceptions for HTTP error statuses.

        Args:
            url (str): The API endpoint URL to fetch data from.

        Returns:
            Any: The JSON response from the API, parsed into Python objects.

        Raises:
            aiohttp.ClientResponseError: If the API returns an HTTP error status
                (e.g., 4xx or 5xx) after retries.
            aiohttp.ClientError: For other client-side errors (e.g., connection issues)
                if they persist after retries.
        """
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        # A new ClientSession is created for each call to _fetch_data.
        # For applications making many calls, a shared session is often preferred for performance
        # (connection pooling). However, for periodic updates as in a coordinator,
        # creating a session per fetch operation or per update cycle can be acceptable.
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return await resp.json()

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Placeholder for fetching tags for a single device.

        Note: This method is defined but not implemented. The actual logic for
        fetching device tags is typically handled by `DeviceTagFetchCoordinator`
        or a similar specific coordinator.

        Args:
            serial (str): The serial number of the device.

        Returns:
            List[str]: An empty list, as this is a placeholder.
        """
        _LOGGER.debug(
            "Placeholder: async_get_device_tags called for serial %s. "
            "Actual tag fetching is handled by a dedicated coordinator.",
            serial
        )
        # The existing logic for fetching tags remains here.
        return [] # Returning empty list as placeholder

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Placeholder for updating tags for a single device.

        Note: This method is defined but not implemented. The actual logic for
        updating device tags is typically handled by `DeviceTagUpdateCoordinator`
        or a similar specific coordinator.

        Args:
            serial (str): The serial number of the device.
            tags (List[str]): The list of tags to apply.
        """
        _LOGGER.debug(
            "Placeholder: async_update_device_tags called for serial %s with tags %s. "
            "Actual tag updating is handled by a dedicated coordinator.",
            serial,
            tags
        )
        # The existing logic for updating tags remains here.
        pass


class MerakiApiConnectionError(Exception):
    """Custom exception raised for errors during connection to the Meraki API.

    This might indicate network issues, DNS failures, or timeouts before a
    response is received.
    """

    pass


class MerakiApiInvalidApiKeyError(Exception):
    """Custom exception raised when the Meraki API key is determined to be invalid.

    This typically results from a 401 Unauthorized response from the API.
    """

    pass
