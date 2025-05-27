"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices, SSIDs, and clients using the Meraki SDK.
"""
import asyncio  # Required for placeholder awaitables
import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from ..meraki_api import MerakiAPIClient
# Assuming your coordinator types are defined, replace Any with them
# if possible
# from .network_coordinator import MerakiNetworkCoordinator
# from .ssid_coordinator import MerakiSsidCoordinator
from ..meraki_api.exceptions import (
    MerakiApiException,
    MerakiApiError,  # This is an alias for MerakiApiException
    MerakiApiConnectionError,
    MerakiApiAuthError, # Use this for API key errors
    MerakiApiNotFoundError, # For 404 errors
    MerakiApiRateLimitError # For 429 errors
)

_LOGGER = logging.getLogger(__name__)

# MERAKI_API_URL is no longer needed as SDK handles URLs.

# Custom exceptions like MerakiApiError, MerakiApiConnectionError, etc.,
# will be replaced by meraki.exceptions.APIError or handled directly.

class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API using the Meraki SDK.

    This class handles the communication with the Meraki API endpoints
    to retrieve various pieces of information required by the integration.
    """

    def __init__(
        self,
        meraki_client: MerakiAPIClient,
        # Consider specific coordinator types if available.
        network_coordinator: Optional[Any] = None,
        # MerakiNetworkCoordinator
        ssid_coordinator: Optional[Any] = None,
        # MerakiSsidCoordinator
    ) -> None:
        """Initialize the MerakiApiDataFetcher.

        Args:
            meraki_client: An instance of the SDK-based MerakiAPIClient.
            network_coordinator: Coordinator for network-related data. (Optional)
            ssid_coordinator: Coordinator for SSID-related data. (Optional)
        """
        self.meraki_client: MerakiAPIClient = meraki_client
        # org_id can be accessed via self.meraki_client.org_id if needed
        self.org_id: str = meraki_client.org_id
        self.network_coordinator: Optional[Any] = network_coordinator
        self.ssid_coordinator: Optional[Any] = ssid_coordinator

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # Retained for potential future use or context.
        # org_id is now available as self.org_id from the client
        # scan_interval: int, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
        # device_name_format: str, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        This method orchestrates calls to retrieve networks, devices, SSIDs,
        and client information using the Meraki SDK.

        Args:
            hass: The Home Assistant instance (currently unused but common pattern).

        Returns:
            A dictionary containing lists of devices, networks, and SSIDs.
            Example: `{"devices": [...], "networks": [...], "ssids": [...]}`.
            The 'devices' list is restructured to include a 'connected_clients' count.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched, preventing a meaningful update.
            MerakiSDKAPIError: For underlying API communication issues from the SDK.
        """
        _LOGGER.debug("Fetching all data for organization ID: %s using SDK", self.org_id)
        # Step 1: Fetch all networks for the organization.
        networks: Optional[List[Dict[str, Any]]] = await self.async_get_networks(
            self.org_id
        )
        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki networks for org {self.org_id}.")

        # Step 2: Fetch all devices for the organization.
        devices: Optional[
            List[Dict[str, Any]]
        ] = await self.async_get_organization_devices(self.org_id)
        if devices is None:
            _LOGGER.error(
                "Could not fetch Meraki devices for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki devices for org {self.org_id}.")

        ssids: List[Dict[str, Any]] = []
        network_clients_data: Dict[str, List[Dict[str, Any]]] = {}

        # Step 3: Iterate through each network to fetch its SSIDs and clients.
        # Define a default timespan for client data, e.g., last 5 minutes (300 seconds)
        # This should ideally be configurable or based on scan_interval.
        # Using a common value like 86400 (1 day) for now, as per typical client data queries.
        # Or use a shorter timespan if only currently connected clients are needed.
        # The original code didn't specify a timespan, SDK might require it or have a default.
        # For getNetworkClients, a timespan is often useful. Let's use 7 days (604800s)
        # or make it configurable. For now, let's assume a timespan of 1 day.
        client_timespan = 86400  # 1 day in seconds

        for network in networks:
            network_id: str = network["id"]
            try:
                # Fetch SSIDs for the current network
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
                ssid_data = await self.async_get_network_ssids(network_id)
                if ssid_data:  # async_get_network_ssids returns [] on 404, None on other errors
                    ssids.extend(ssid_data)
                elif ssid_data is None: # Indicates an actual error other than 404
                    _LOGGER.warning("SSID data was None for network %s, skipping SSID processing for this network.", network_id)


                # Fetch clients for the current network
                _LOGGER.debug("Fetching clients for network ID: %s", network_id)
                # The `meraki` library handles pagination automatically.
                current_network_clients = await self.meraki_client.networks.get_network_clients(
                    network_id=network_id,
                    timespan=client_timespan,
                )
                if current_network_clients:
                    network_clients_data[network_id] = (
                        current_network_clients
                        if isinstance(current_network_clients, list)
                        else [current_network_clients]
                    )
            except MerakiSDKAPIError as e:
                _LOGGER.warning(
                    "SDK API error during data fetch for network %s (SSIDs or Clients): %s. Status: %s, Reason: %s. Skipping this network's details.",
                    network_id,
                    e,
                    e.status,
                    e.reason
                )
                # If it was a 404 for SSIDs, async_get_network_ssids already handled it by returning [].
                # Other errors (e.g., for clients, or non-404 for SSIDs) will result in skipping.
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Unexpected error fetching SSIDs or client data for network %s: %s. Skipping.",
                    network_id,
                    e,
                )

        # Step 4: Restructure device data
        restructured_devices: List[Dict[str, Any]] = []
        for device in devices:  # devices is not None here
            device_info = device.copy()
            connected_clients_count = 0
            device_network_id = device_info.get("networkId")
            device_serial = device_info.get("serial")

            if device_network_id and device_network_id in network_clients_data:
                connected_clients_count = sum(
                    1
                    for client in network_clients_data[device_network_id]
                    # SDK output structure for client:
                    # Check Meraki SDK docs for exact field names.
                    # Assuming 'recentDeviceSerial' or 'recentDeviceMac' and 'status' exist.
                    # Let's assume client objects from SDK are dicts.
                    if client.get("recentDeviceSerial") == device_serial # or client.get("recentDeviceMac")
                    and client.get("status") == "Online"
                )
            device_info["connected_clients"] = connected_clients_count
            restructured_devices.append(device_info)

        # Step 5: Return the aggregated data
        return {
            "devices": restructured_devices,
            "networks": networks,
            "ssids": ssids,
        }

    async def async_get_networks(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.networks.get_organization_networks(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK."""
        _LOGGER.debug("Fetching organization devices for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.devices.get_organization_devices(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching devices for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching devices for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK."""
        _LOGGER.debug("Fetching SSIDs for network ID: %s using SDK", network_id)
        try:
            return await self.meraki_client.wireless.get_network_wireless_ssids(
                network_id=network_id
            )
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for ntwk %s (no wireless capabilities or SSIDs via SDK), returning empty list.",
                    network_id,
                )
                return []  # Treat 404 as "no SSIDs found"
            _LOGGER.warning(
                "SDK API error fetching SSIDs for ntwk %s: %s. Returning None for this network's SSIDs.",
                network_id,
                e,
            )
            # Depending on desired behavior, could return None or empty list for other errors
            return None # Or [] if preferred to not block other network processing
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for ntwk %s: %s. Returning None.",
                network_id,
                e,
            )
            return None

    # _fetch_data method is no longer needed.

    async def async_get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single device by its serial number.

        Note: This method might be redundant if device tags are included in
        the main organization devices API response or if using SDK device objects.
        The Meraki SDK's device objects might already contain tags.
        If direct SDK call is needed: `self.meraki_client.devices.get_device_tags(serial)`
        """
        _LOGGER.debug("Attempting to fetch tags for device serial: %s using SDK", serial)
        try:
            # This is an example, actual SDK method might differ or not exist.
            # tags_data = await self.meraki_client.devices.get_device_tags(serial=serial) # Fictional method
            # For now, assuming tags are part of the device object from get_organization_devices
            # or this function needs specific SDK call if available.
            # The 'meraki' library has: devices.getDeviceApplianceUplinksSettings (not tags)
            # devices.getDeviceWirelessBluetoothSettings (not tags)
            # The standard getOrganizationDevices call should include tags if the API provides them.
            # If tags are fetched per device, it's usually:
            # `await self.meraki_client.devices.get_device(serial=serial)` then parse tags.
            # Or if there's a specific tags endpoint:
            # `await self.meraki_client.devices.get_device_tags(serial=serial)` - this depends on SDK implementation.
            # Let's assume for now it's not a direct SDK call and this method is lower priority.
            _LOGGER.warning(
                "async_get_device_tags logic using SDK needs verification. Serial: %s",
                serial,
            )
            # Placeholder implementation, actual SDK call for tags needed.
            # Example: device_details = await self.meraki_client.devices.get_device(serial)
            # return device_details.get('tags', [])
            await asyncio.sleep(0)
            return []
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching tags for device %s: %s. Returning empty list.", serial, e
            )
            return []
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching tags for device %s: %s. Returning empty list.", serial, e
            )
            return []


    async def async_update_device_tags(self, serial: str, tags: List[str]) -> bool:
        """Update tags for a single device by its serial number using the SDK.
        Note: Actual SDK method: `self.meraki_client.devices.update_device(serial, tags=tags)` (example)
        """
        _LOGGER.debug("Attempting to update tags for device serial: %s to %s using SDK", serial, tags)
        try:
            # Example: await self.meraki_client.devices.update_device(serial, tags=tags)
            # The 'meraki' library has: devices.updateDevice(serial, tags=tags_list_as_string)
            # The SDK expects tags as a space-separated string for updateDevice.
            tags_str = " ".join(tags)
            await self.meraki_client.devices.update_device(serial=serial, tags=tags_str)
            _LOGGER.info("Successfully updated tags for device %s to %s", serial, tags_str)
            return True
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                "SDK API error updating tags for device %s: %s", serial, e
            )
            return False
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error updating tags for device %s: %s", serial, e
            )
            return False
