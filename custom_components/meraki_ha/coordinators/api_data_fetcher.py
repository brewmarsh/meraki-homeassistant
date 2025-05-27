"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices (including tags), SSIDs, and device-specific details
like client counts and radio settings for MR devices, using the Meraki SDK.
"""
import asyncio
import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from custom_components.meraki_ha.meraki_api import MerakiAPIClient
# Obsolete imports for MerakiApiException and related custom exceptions are removed
# as MerakiSDKAPIError from meraki.exceptions is used directly.

_LOGGER = logging.getLogger(__name__)

# MERAKI_API_URL is no longer needed as SDK handles URLs.
# Custom exceptions like MerakiApiError, MerakiApiConnectionError, etc.,
# are replaced by meraki.exceptions.APIError or handled directly.

class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API using the Meraki SDK.

    This class handles communication with the Meraki API to retrieve
    networks, devices (with tags), SSIDs, and for MR devices, client counts
    and radio settings. It uses an instance of `MerakiAPIClient` for all
    API interactions.
    """

    def __init__(
        self,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the MerakiApiDataFetcher.

        Args:
            meraki_client: An instance of the SDK-based `MerakiAPIClient`.
        """
        self.meraki_client: MerakiAPIClient = meraki_client
        self.org_id: str = meraki_client.org_id # Organization ID from the client

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # hass is retained for potential future use or context.
        # Other parameters like org_id, scan_interval, device_name_format
        # are no longer passed here as org_id comes from self.org_id
        # and others are not directly used in this method's revised logic.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        This method orchestrates calls to retrieve networks, devices (including their tags),
        SSIDs. For MR (wireless access point) devices, it additionally fetches the
        connected client count and wireless radio settings using concurrent tasks.

        Args:
            hass: The Home Assistant instance (currently unused but common pattern).

        Returns:
            A dictionary containing lists of devices, networks, and SSIDs.
            Example: `{"devices": [...], "networks": [...], "ssids": [...]}`.
            The 'devices' list includes tags, and for MR devices, it also includes
            `connected_clients_count` and `radio_settings`.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched after retries/error handling within helper methods,
                          preventing a meaningful update.
            MerakiSDKAPIError: For underlying API communication issues from the SDK
                               that are not handled by individual fetch methods and
                               escalate to this level.
        """
        _LOGGER.debug("Fetching all data for organization ID: %s using SDK", self.org_id)
        
        # Step 1: Fetch all networks for the organization.
        # `async_get_networks` handles its own exceptions and returns None on failure.
        networks: Optional[List[Dict[str, Any]]] = None
        try:
            networks = await self.async_get_networks(self.org_id)
        except MerakiSDKAPIError as e: # Should be caught by async_get_networks, but as a safeguard
            _LOGGER.error(
                "Critical error fetching networks for org %s: %s. This should have been handled by async_get_networks.",
                self.org_id,
                e,
            )
            # networks remains None
        
        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki networks for org {self.org_id}.")

        # Step 2: Fetch all devices for the organization.
        # `async_get_organization_devices` handles its own exceptions.
        devices: Optional[List[Dict[str, Any]]] = None
        try:
            devices = await self.async_get_organization_devices(self.org_id)
        except MerakiSDKAPIError as e: # Safeguard
            _LOGGER.error(
                "Critical error fetching devices for org %s: %s. This should have been handled by async_get_organization_devices.",
                self.org_id,
                e,
            )
            # devices remains None

        if devices is None:
            _LOGGER.error(
                "Could not fetch Meraki devices for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki devices for org {self.org_id}.")

        # Step 2a: Fetch additional details for MR devices (client count and radio settings).
        # This involves creating a list of asynchronous tasks for MR devices.
        mr_device_tasks = []
        for device in devices: # `devices` is confirmed not None here.
            if device.get("model", "").upper().startswith("MR"):
                serial = device["serial"] # Assumes 'serial' is always present for MR devices.
                mr_device_tasks.append(self._async_get_mr_device_details(device, serial))

        if mr_device_tasks:
            await asyncio.gather(*mr_device_tasks)
            # Results of these tasks (client counts, radio settings) are directly updated
            # in the respective device dictionaries within the `devices` list.

        ssids: List[Dict[str, Any]] = []
        # The `network_clients_data` dictionary is no longer needed here as client counting
        # for MR devices is handled by `_async_get_mr_device_details`.
        # If a list of all clients per network was needed elsewhere, it would be collected here.

        # Step 3: Iterate through each network to fetch its SSIDs.
        # `async_get_network_ssids` handles its own exceptions.
        for network in networks: # `networks` is confirmed not None here.
            network_id: str = network["id"] # Assumes 'id' is always present.
            try:
                # Fetch SSIDs for the current network.
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
                ssid_data_for_network = None # Initialize for clarity.
                try:
                    ssid_data_for_network = await self.async_get_network_ssids(network_id)
                except MerakiSDKAPIError as e: # Should be caught by async_get_network_ssids
                    _LOGGER.warning(
                        "Error fetching SSIDs for network %s was not handled by async_get_network_ssids: %s. Status: %s, Reason: %s. Skipping.",
                        network_id, e, e.status, e.reason,
                    )
                    # ssid_data_for_network remains None.
                
                if ssid_data_for_network:  # `async_get_network_ssids` returns [] on 404, None on other errors.
                    ssids.extend(ssid_data_for_network)
                elif ssid_data_for_network is None: # Indicates an error handled by async_get_network_ssids or the safeguard above.
                    _LOGGER.info("SSID data result was None for network %s, SSIDs for this network will be skipped.", network_id)

            except Exception as e:  # pylint: disable=broad-except
                # This catches unexpected errors not already handled by MerakiSDKAPIError
                # during the loop's own logic, not from `async_get_network_ssids` itself.
                _LOGGER.exception(
                    "Unexpected error processing network %s for SSID data: %s. Skipping this network's SSIDs.",
                    network_id, e,
                )

        # Step 4: Restructuring of device data (e.g., `restructured_devices`) is no longer performed here.
        # The `devices` list, now augmented with MR-specific details, is returned directly.

        # Step 5: Return the aggregated data.
        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
        }

    async def _async_get_mr_device_details(self, device: Dict[str, Any], serial: str) -> None:
        """Asynchronously fetch and store client count and radio settings for an MR device.

        This helper method updates the provided `device` dictionary in-place with
        `connected_clients_count` and `radio_settings`. It handles API errors
        gracefully by logging them and setting default values.

        Args:
            device: The dictionary representing the MR device to update.
            serial: The serial number of the MR device.
        """
        # Fetch connected client count
        try:
            clients_data = await self.meraki_client.devices.get_device_clients(serial=serial)
            device["connected_clients_count"] = len(clients_data) if clients_data else 0
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch client count for MR device %s (Serial: %s): API Error %s - %s. Setting client count to 0.",
                device.get("name", "Unknown"), serial, e.status, e.reason,
            )
            device["connected_clients_count"] = 0
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching client count for MR device %s (Serial: %s): %s. Setting client count to 0.",
                device.get("name", "Unknown"), serial, e,
            )
            device["connected_clients_count"] = 0

        # Fetch wireless radio settings
        try:
            radio_settings = await self.meraki_client.wireless.get_device_wireless_radio_settings(serial=serial)
            device["radio_settings"] = radio_settings
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch radio settings for MR device %s (Serial: %s): API Error %s - %s. Setting radio settings to None.",
                device.get("name", "Unknown"), serial, e.status, e.reason,
            )
            device["radio_settings"] = None
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching radio settings for MR device %s (Serial: %s): %s. Setting radio settings to None.",
                device.get("name", "Unknown"), serial, e,
            )
            device["radio_settings"] = None


    async def async_get_networks(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK.

        Args:
            org_id: The organization ID for which to fetch networks.

        Returns:
            A list of network dictionaries if successful, None otherwise.
            Handles `MerakiSDKAPIError` and other exceptions internally.
        """
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.networks.get_organization_networks(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching networks for org %s: Status %s, Reason: %s. Returning None.",
                org_id, e.status, e.reason,
            )
            return None
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching networks for org %s: %s. Returning None.",
                org_id, e,
            )
            return None

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK.

        Args:
            org_id: The organization ID for which to fetch devices.

        Returns:
            A list of device dictionaries if successful, None otherwise.
            Handles `MerakiSDKAPIError` and other exceptions internally.
        """
        _LOGGER.debug("Fetching organization devices for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.devices.get_organization_devices(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching devices for org %s: Status %s, Reason: %s. Returning None.",
                org_id, e.status, e.reason,
            )
            return None
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching devices for org %s: %s. Returning None.",
                org_id, e,
            )
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK.

        Args:
            network_id: The network ID for which to fetch SSIDs.

        Returns:
            A list of SSID dictionaries if successful. Returns an empty list
            if the network has no SSIDs (HTTP 404) or None if another error occurs.
            Handles `MerakiSDKAPIError` and other exceptions internally.
        """
        _LOGGER.debug("Fetching SSIDs for network ID: %s using SDK", network_id)
        try:
            return await self.meraki_client.wireless.get_network_wireless_ssids(
                network_id=network_id
            )
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for network %s (likely no wireless capabilities or SSIDs configured). Returning empty list.",
                    network_id,
                )
                return []  # Treat 404 as "no SSIDs found" for this network.
            _LOGGER.warning(
                "SDK API error fetching SSIDs for network %s: Status %s, Reason: %s. Returning None for this network's SSIDs.",
                network_id, e.status, e.reason,
            )
            return None # Indicates an error occurred, distinct from an empty list for 404.
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for network %s: %s. Returning None.",
                network_id, e,
            )
            return None

    # The _fetch_data method, previously part of a different API client structure, is no longer needed.
