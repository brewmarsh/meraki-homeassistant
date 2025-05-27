"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices, SSIDs, and clients. It also defines custom
exception classes for API-related errors.
"""
import asyncio  # Required for placeholder awaitables
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
# Assuming your coordinator types are defined, replace Any with them
# if possible
# from .network_coordinator import MerakiNetworkCoordinator
# from .ssid_coordinator import MerakiSsidCoordinator

_LOGGER = logging.getLogger(__name__)

MERAKI_API_URL: str = "https://api.meraki.com/api/v1"
"""Base URL for the Meraki Dashboard API."""


class MerakiApiError(Exception):
    """Base class for exceptions raised by the Meraki API client.

    This exception is a generic base for more specific API errors.
    """

    pass


class MerakiApiConnectionError(MerakiApiError):
    """Exception raised for errors when connecting to the Meraki API.

    This typically indicates network issues or problems reaching the API endpoint.
    """

    pass


class MerakiApiInvalidApiKeyError(MerakiApiError):
    """Exception raised when the Meraki API key is invalid or unauthorized.

    Occurs if API key lacks permissions or is incorrect.
    """

    pass


class MerakiApiSsidFetchError(MerakiApiError):
    """Exception raised when fetching SSIDs from a network fails.

    May happen if a network doesn't support wireless SSIDs or if
    there's an issue retrieving SSID information.
    """

    pass


class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API.

    This class handles the communication with the Meraki API endpoints
    to retrieve various pieces of information required by the integration.
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        # Consider specific coordinator types if available.
        network_coordinator: Optional[Any] = None,
        # MerakiNetworkCoordinator
        ssid_coordinator: Optional[Any] = None,
        # MerakiSsidCoordinator
    ) -> None:
        """Initialize the MerakiApiDataFetcher.

        Args:
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            network_coordinator: Coordinator for network-related data. (Optional)
            ssid_coordinator: Coordinator for SSID-related data. (Optional)
        """
        self.api_key: str = api_key
        self.org_id: str = org_id
        self.network_coordinator: Optional[Any] = network_coordinator
        self.ssid_coordinator: Optional[Any] = ssid_coordinator
        # base_url is specific to an organization, consider if it should be
        # a method param or if this class is always org-specific.
        # self.base_url: str = f"{MERAKI_API_URL}/organizations/{org_id}"
        # The `base_url` was previously defined here but not consistently used.
        # API calls now construct full URLs or use the `_fetch_data` helper
        # which takes a full URL. This simplifies the constructor and makes
        # endpoint management more explicit in each method.

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # Retained for potential future use or context.
        org_id: str,
        # scan_interval: int, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
        # device_name_format: str, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        This method orchestrates calls to retrieve networks, devices, SSIDs,
        and client information. It serves as a central point for gathering
        all data required by the integration at each update interval.

        Args:
            hass: The Home Assistant instance (currently unused but common pattern).
            org_id: The Meraki Organization ID for which to fetch data.

        Returns:
            A dictionary containing lists of devices, networks, and SSIDs.
            Example: `{"devices": [...], "networks": [...], "ssids": [...]}`.
            The 'devices' list is restructured to include a 'connected_clients' count.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched, preventing a meaningful update.
            MerakiApiError: For underlying API communication issues not
                            caught as UpdateFailed.
        """
        _LOGGER.debug("Fetching all data for organization ID: %s", org_id)
        # Step 1: Fetch all networks for the organization.
        # This is a foundational piece of data, as devices and SSIDs are
        # often network-specific.
        networks: Optional[List[Dict[str, Any]]] = await self.async_get_networks(
            org_id
        )
        # If network fetching fails (returns None), it's a critical failure
        # for data update.
        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                org_id,
            )
            raise UpdateFailed("Could not fetch Meraki networks.")

        # Step 2: Fetch all devices for the organization.
        # This provides the list of all hardware managed by Meraki.
        devices: Optional[
            List[Dict[str, Any]]
        ] = await self.async_get_organization_devices(org_id)
        # If device fetching fails, it's also considered a critical failure.
        if devices is None:
            _LOGGER.error(
                "Could not fetch Meraki devices for org ID: %s. Aborting update.",
                org_id,
            )
            raise UpdateFailed("Could not fetch Meraki devices.")

        # Initialize lists/dicts to store aggregated data from per-network calls.
        ssids: List[Dict[str, Any]] = []  # Stores all SSIDs.
        network_clients: Dict[str, List[Dict[str, Any]]] = (
            {}
        )  # Stores clients, keyed by network_id.

        # Step 3: Iterate through each network to fetch its SSIDs and clients.
        for network in networks:  # `networks` is confirmed not None here.
            network_id: str = network["id"]  # Get the current network's ID.
            try:
                # Fetch SSIDs for the current network.
                # `async_get_network_ssids` can return None or an empty list
                # on non-critical errors for a single network.
                ssid_data = await self.async_get_network_ssids(network_id)
                if ssid_data:  # Only extend if not None and not empty.
                    ssids.extend(ssid_data)

                # Fetch clients for the current network.
                # The `_fetch_data` method is used directly here.
                clients_url = f"{MERAKI_API_URL}/networks/{network_id}/clients"
                clients_data = await self._fetch_data(clients_url)
                if clients_data:  # Only add if not None and not empty.
                    network_clients[network_id] = clients_data
            # Handle errors specific to fetching SSIDs for one network.
            except MerakiApiSsidFetchError:
                _LOGGER.warning(
                    "Could not fetch SSIDs for ntwk %s, skipping for this ntwk.",
                    network_id,
                )
            # Handle HTTP response errors (e.g., 403, 500) for clients.
            except aiohttp.ClientResponseError as e:
                _LOGGER.warning(
                    "API error for client data ntwk %s: %s - %s. Skipping.",
                    network_id,
                    e.status,
                    e.message,
                )
            # Handle other client-side connection errors for clients.
            except aiohttp.ClientError as e:
                _LOGGER.error(
                    "Client error for client data ntwk %s: %s. Skipping.",
                    network_id,
                    e,
                )
            # Handle API errors from `_fetch_data` for clients.
            except MerakiApiError as e:
                _LOGGER.error(
                    "Meraki API error for client data ntwk %s: %s. Skipping.",
                    network_id,
                    e,
                )
            # Catch any other unexpected exceptions during per-network fetching.
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception(  # Use .exception for stack trace
                    "Unexpected error for client data ntwk %s: %s. Skipping.",
                    network_id,
                    e,
                )

        # Step 4: Restructure device data to include a count of connected
        # clients for each device. This adds valuable context.
        restructured_devices: List[Dict[str, Any]] = []
        for device in devices:  # `devices` is confirmed not None here.
            device_info = device.copy()  # Work on a copy.
            connected_clients_count = 0  # Default to 0.
            device_network_id = device_info.get(
                "networkId"
            )  # Network device belongs to.
            device_serial = device_info.get("serial")  # Device's serial.

            # Check if client data was fetched for this device's network.
            if device_network_id and device_network_id in network_clients:
                # Sum clients where 'recentDeviceSerial' matches current
                # device's serial and status is "Online".
                connected_clients_count = sum(
                    1  # Count each client matching criteria.
                    for client in network_clients[device_network_id]
                    if client.get("recentDeviceSerial") == device_serial
                    and client.get("status") == "Online"  # Client is online.
                )
            # Add the count to the device info.
            device_info["connected_clients"] = connected_clients_count
            restructured_devices.append(device_info)

        # Step 5: Return the aggregated and restructured data.
        # This dictionary forms the main data object for the coordinator.
        return {
            "devices": restructured_devices,  # Devices with client counts.
            "networks": networks,  # Original list of networks.
            "ssids": ssids,  # Aggregated list of all SSIDs.
        }

    async def async_get_networks(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization.

        Args:
            org_id: The Meraki Organization ID.

        Returns:
            A list of dictionaries, where each dictionary represents a network,
            or None if an error occurs preventing data retrieval.

        Raises:
            MerakiApiError: For underlying API communication issues from
                            `_fetch_data` not handled by returning None.
        """
        # Construct the API URL for fetching networks within an organization.
        url = f"{MERAKI_API_URL}/organizations/{org_id}/networks"
        _LOGGER.debug("Fetching networks from URL: %s", url)
        try:
            # Use the internal _fetch_data helper to make the API call.
            return await self._fetch_data(url)
        except MerakiApiError as e:  # Catch API errors specifically.
            _LOGGER.warning(
                "API error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None  # Indicate failure to the caller.
        except Exception as e:  # Catch any other unexpected errors.
            _LOGGER.exception(  # Log with stack trace
                "Unexpected error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None  # Indicate failure.

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization.

        Args:
            org_id: The Meraki Organization ID.

        Returns:
            A list of dictionaries, where each dictionary represents a device,
            or None if an error occurs preventing data retrieval.

        Raises:
            MerakiApiError: For underlying API communication issues from
                            `_fetch_data`.
        """
        # Construct the API URL for fetching all devices within an organization.
        url = f"{MERAKI_API_URL}/organizations/{org_id}/devices"
        _LOGGER.debug("Fetching organization devices from URL: %s", url)
        try:
            # Use the internal _fetch_data helper.
            return await self._fetch_data(url)
        except MerakiApiError as e:  # Specific API error handling.
            _LOGGER.warning(
                "API error fetching devices for org %s from %s: %s. Returning None.",
                org_id,
                url,
                e,
            )
            return None
        except Exception as e:  # Catch-all for other issues.
            _LOGGER.exception(
                "Unexpected error fetching devices for org %s from %s: %s. "
                "Returning None.",
                org_id,
                url,
                e,
            )
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents an SSID.
            Returns an empty list if the network is not found (HTTP 404) or if it
            has no wireless capabilities/SSIDs configured (which can also
            result in a 404 or an empty list from the API depending on the
            network type). Returns None for other critical errors.

        Raises:
            MerakiApiSsidFetchError: If fetching SSIDs fails due to API
                reasons other than 404 (e.g., 403 Forbidden, 500 Server Error).
            MerakiApiConnectionError: For client-side connection issues.
            MerakiApiError: For other underlying errors not fitting the
                            above, or if re-raised.
        """
        # Construct the API URL for fetching SSIDs for a given network.
        url = f"{MERAKI_API_URL}/networks/{network_id}/wireless/ssids"
        _LOGGER.debug("Fetching SSIDs from URL: %s", url)
        try:
            # Use the internal _fetch_data helper.
            return await self._fetch_data(url)
        # Handle specific HTTP errors that might occur for this endpoint.
        except aiohttp.ClientResponseError as e:
            # Errors raised by `resp.raise_for_status()` in _fetch_data
            _LOGGER.warning(
                "API response error fetching SSIDs for ntwk %s from %s: %s - %s",
                network_id,
                url,
                e.status,  # HTTP status code
                e.message,  # Error message from response or reason phrase
            )
            # If resource not found (404), it's often not a critical error
            # for this call; it might mean no wireless features or SSIDs.
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for ntwk %s (no wireless "
                    "capabilities or SSIDs), returning empty list.",
                    network_id,
                )
                return []  # Treat 404 as "no SSIDs found".
            # For other HTTP errors (e.g., 401, 403, 5xx), raise specific error.
            raise MerakiApiSsidFetchError(
                f"Failed to fetch SSIDs for ntwk {network_id}: {e.status} - "
                f"{e.message}"
            ) from e
        # Handle client-side connection errors (e.g., DNS, TCP).
        except aiohttp.ClientError as e:
            _LOGGER.error(
                "Client error fetching SSIDs for ntwk %s from %s: %s",
                network_id,
                url,
                e,
            )
            # Wrap in a custom connection error type.
            raise MerakiApiConnectionError(
                f"Client error fetching SSIDs for ntwk {network_id}: {e}"
            ) from e
        # Re-raise if _fetch_data already wrapped it in MerakiApiError.
        except MerakiApiError:
            raise
        # Catch any other unexpected Python exceptions.
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for ntwk %s from %s: %s",
                network_id,
                url,
                e,
            )
            # Wrap unexpected errors in a generic MerakiApiError.
            raise MerakiApiError(
                f"Unexpected error fetching SSIDs for ntwk {network_id}: {e}"
            ) from e

    async def _fetch_data(self, url: str) -> Any:
        """Fetch data from a given URL using aiohttp.

        This is a generic helper method for making GET requests to the Meraki API.
        It centralizes request logic, header setup, and basic error handling.

        Args:
            url: The URL to fetch data from.

        Returns:
            The JSON response from the API, typically as a Python dictionary or list.
            The exact type depends on the API endpoint's response.

        Raises:
            MerakiApiInvalidApiKeyError: If API responds with 401 Unauthorized.
            MerakiApiConnectionError: If client-side connection error occurs
                                      (e.g., DNS failure, timeout).
            MerakiApiError: For other HTTP status codes indicating an API error
                            (400, 5xx range) or if JSON decoding fails.
        """
        # Standard headers for Meraki API requests.
        headers: Dict[str, str] = {
            "X-Cisco-Meraki-API-Key": self.api_key,  # API key for auth.
            "Content-Type": "application/json",  # Request body format (GET none).
            "Accept": "application/json",  # Preferred response format.
        }
        # Log the request, masking the API key for security.
        masked_headers = {
            k: (v if k != "X-Cisco-Meraki-API-Key" else "****")
            for k, v in headers.items()
        }
        _LOGGER.debug(
            "Fetching data from URL: %s with headers: %s", url, masked_headers
        )
        try:
            # Create a new client session for each request.
            # Consider a shared session for performance if appropriate.
            async with aiohttp.ClientSession() as session:
                # Make GET request with headers and a 10s timeout.
                async with session.get(
                    url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    _LOGGER.debug("Response status from %s: %s", url, resp.status)
                    # Handle 401 Unauthorized (API key issue).
                    if resp.status == 401:
                        _LOGGER.error(
                            "Meraki API request unauthorized (401) for URL: %s. "
                            "Check API key permissions.",
                            url,
                        )
                        raise MerakiApiInvalidApiKeyError(
                            f"API key invalid or unauthorized for {url}"
                        )
                    # For other error statuses (400-599), raise.
                    # This will be caught by aiohttp.ClientResponseError.
                    resp.raise_for_status()
                    # Attempt to parse the response as JSON.
                    return await resp.json()
        # Handle HTTP errors raised by `resp.raise_for_status()`.
        except aiohttp.ClientResponseError as e:
            _LOGGER.error(
                "Meraki API HTTP error %s for URL %s: %s",
                e.status,
                url,
                e.message,
            )
            # Wrap in a generic MerakiApiError.
            raise MerakiApiError(
                f"API request to {url} failed with status {e.status}: {e.message}",
                status_code=e.status,
            ) from e
        # Handle errors related to establishing a connection (e.g., DNS).
        except aiohttp.ClientConnectionError as e:
            _LOGGER.error("Meraki API connection error for URL %s: %s", url, e)
            # Wrap in a specific connection error type.
            raise MerakiApiConnectionError(
                f"Connection error while trying to reach {url}: {e}"
            ) from e
        # Handle other aiohttp client-side errors.
        except aiohttp.ClientError as e:
            _LOGGER.error("Meraki API client error for URL %s: %s", url, e)
            raise MerakiApiError(
                f"Client error during API request to {url}: {e}"
            ) from e
        # Catch other exceptions (e.g., JSONDecodeError).
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error during _fetch_data for URL %s: %s", url, e
            )
            # Wrap in a generic MerakiApiError.
            raise MerakiApiError(
                f"Unexpected error processing request to {url}: {e}"
            ) from e

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single device by its serial number.

        Note: This method might be redundant if device tags are included in
        the main organization devices API response.

        Args:
            serial: The serial number of the device.

        Returns:
            A list of tags associated with the device. Returns an empty list
            if the device has no tags or if an error occurs.

        Raises:
            MerakiApiError: For underlying API communication issues.
        """
        # Example URL, adjust if needed:
        # url = f"{MERAKI_API_URL}/devices/{serial}/tags"
        # _LOGGER.debug("Fetching tags for device serial: %s from URL: %s", serial, url)
        # try:
        #     tags_data = await self._fetch_data(url)
        #     return tags_data if isinstance(tags_data, list) else []
        # except MerakiApiError as e:
        #     _LOGGER.warning(
        #         "API error fetching tags for device %s: %s. Returning empty list.", serial, e
        #     )
        #     return []
        _LOGGER.warning(
            "async_get_device_tags is not fully implemented yet. Serial: %s",
            serial,
        )
        # Placeholder implementation
        await asyncio.sleep(0)  # Make it awaitable
        return []  # Return empty list as per original pass

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> bool:
        """Update tags for a single device by its serial number.

        Note: This method might be redundant if device tags can be updated via
        other means or are managed differently.

        Args:
            serial: The serial number of the device.
            tags: A list of tags to set for the device. Existing tags might
                  be overwritten.

        Returns:
            True if the tags were updated successfully, False otherwise.

        Raises:
            MerakiApiError: For underlying API communication issues.
        """
        # Example URL, adjust if needed:
        # url = f"{MERAKI_API_URL}/devices/{serial}/tags"
        # payload = tags # Or however the API expects the tags
        # _LOGGER.debug("Updating tags for device serial: %s to %s via URL: %s", serial, tags, url)
        # try:
        #     # Assuming _put_data or similar method exists for PUT requests
        #     # await self._put_data(url, payload)
        #     # return True
        # except MerakiApiError as e:
        #     _LOGGER.error(
        #         "API error updating tags for device %s: %s", serial, e
        #     )
        #     return False
        _LOGGER.warning(
            "async_update_device_tags is not fully implemented yet. "
            "Serial: %s, Tags: %s",
            serial,
            tags,
        )
        # Placeholder implementation
        await asyncio.sleep(0)  # Make it awaitable
        return False  # Return False as per original pass
