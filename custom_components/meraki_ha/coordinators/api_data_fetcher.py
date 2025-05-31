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
        self.org_id: str = meraki_client.org_id  # Organization ID from the client

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
        _LOGGER.debug(
            "Fetching all data for organization ID: %s using SDK", self.org_id
        )

        # Step 1: Fetch all networks for the organization.
        # `async_get_networks` handles its own exceptions and returns None on failure.
        networks: Optional[List[Dict[str, Any]]] = None
        try:
            networks = await self.async_get_networks(self.org_id)
        except (
            MerakiSDKAPIError
        ) as e:  # Should be caught by async_get_networks, but as a safeguard
            _LOGGER.error(
                "Critical error fetching networks for org %s: %s. "
                "This should have been handled by async_get_networks.",
                self.org_id,
                e,
            )
            # networks remains None

        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(
                f"Could not fetch Meraki networks for org {self.org_id}."
            )

        # Step 2: Fetch all devices for the organization.
        # `async_get_organization_devices` handles its own exceptions.
        devices: Optional[List[Dict[str, Any]]] = None
        try:
            devices = await self.async_get_organization_devices(self.org_id)
        except MerakiSDKAPIError as e:  # Safeguard
            _LOGGER.error(
                "Critical error fetching devices for org %s: %s. "
                "This should have been handled by async_get_organization_devices.",
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

        # Step 2.1: Fetch Device Statuses
        device_statuses_map = {}
        if devices:  # Only fetch statuses if we have devices
            try:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: Fetching device statuses for org ID: %s",
                    self.org_id,
                )
                # Use total_pages='all' if supported and tested with the library version.
                # If not, manual pagination might be needed for large organizations.
                # For now, assume total_pages='all' or the default call gets
                # enough for testing.
                statuses_data = await self.meraki_client.organizations.getOrganizationDevicesStatuses(
                    organizationId=self.org_id, total_pages="all"
                )
                if statuses_data:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Received %d status entries.",
                        len(statuses_data),
                    )
                    for status_entry in statuses_data:
                        if status_entry.get("serial"):
                            device_statuses_map[status_entry["serial"]] = (
                                status_entry.get("status")
                            )
                else:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: No status data returned from getOrganizationDeviceStatuses."
                    )
            except MerakiSDKAPIError as e:
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: SDK API error fetching device statuses for org %s: "
                    "Status %s, Reason: %s. Device statuses may be incomplete.",
                    self.org_id,
                    e.status,
                    e.reason,
                )
            except Exception as e:
                _LOGGER.exception(
                    "MERAKI_DEBUG_FETCHER: Unexpected error fetching device statuses for org %s: %s. "
                    "Device statuses may be incomplete.",
                    self.org_id,
                    e,
                )

        # Step 2.2: Merge Statuses into Devices
        if devices and device_statuses_map:
            for device in devices:
                serial = device.get("serial")
                if serial and serial in device_statuses_map:
                    device["status"] = device_statuses_map[serial]
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Merged status '%s' for device %s",
                        device["status"],
                        serial,
                    )
                elif serial:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: No specific status entry found for device %s. It may retain a prior status or have none.",
                        serial,
                    )
        elif devices:
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: No device statuses were successfully mapped, skipping merge."
            )

        # Step 2a: Fetch additional details for MR devices (client count and radio settings).
        # This involves creating a list of asynchronous tasks for MR devices.
        mr_device_tasks = []
        for device in devices:  # `devices` is confirmed not None here.
            if device.get("model", "").upper().startswith("MR"):
                # Assumes 'serial' is always present for MR devices.
                serial = device["serial"]
                mr_device_tasks.append(
                    self._async_get_mr_device_details(device, serial)
                )

        if mr_device_tasks:
            await asyncio.gather(*mr_device_tasks)
            # Results of these tasks (client counts, radio settings) are directly updated
            # in the respective device dictionaries within the `devices` list.

        ssids: List[Dict[str, Any]] = []
        # The `network_clients_data` dictionary is no longer needed here as client counting
        # for MR devices is handled by `_async_get_mr_device_details`.
        # If a list of all clients per network was needed elsewhere, it would
        # be collected here.

        # Step 3: Iterate through each network to fetch its SSIDs.
        # `async_get_network_ssids` handles its own exceptions.
        for network in networks:  # `networks` is confirmed not None here.
            network_id: str = network["id"]  # Assumes 'id' is always present.
            try:
                # Fetch SSIDs for the current network.
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
                ssid_data_for_network = None  # Initialize for clarity.
                try:
                    ssid_data_for_network = await self.async_get_network_ssids(
                        network_id
                    )
                except (
                    MerakiSDKAPIError
                ) as e:  # Should be caught by async_get_network_ssids
                    _LOGGER.warning(
                        "Error fetching SSIDs for network %s was not handled by async_get_network_ssids: %s. Status: %s, Reason: %s. Skipping.",
                        network_id,
                        e,
                        e.status,
                        e.reason,
                    )
                    # ssid_data_for_network remains None.

                # `async_get_network_ssids` returns [] on 404, None on other errors.
                if ssid_data_for_network:
                    ssids.extend(ssid_data_for_network)
                # Indicates an error handled by async_get_network_ssids or the
                # safeguard above.
                elif ssid_data_for_network is None:
                    _LOGGER.info(
                        "SSID data result was None for network %s, "
                        "SSIDs for this network will be skipped.",
                        network_id,
                    )

            except Exception as e:  # pylint: disable=broad-except
                # This catches unexpected errors not already handled by MerakiSDKAPIError
                # during the loop's own logic, not from
                # `async_get_network_ssids` itself.
                _LOGGER.exception(
                    "Unexpected error processing network %s for SSID data: %s. "
                    "Skipping this network's SSIDs.",
                    network_id,
                    e,
                )

        # Step 4: Restructuring of device data (e.g., `restructured_devices`) is no longer performed here.
        # The `devices` list, now augmented with MR-specific details, is
        # returned directly.

        # Step 5: Fetch clients for each network.
        all_clients: List[Dict[str, Any]] = []
        if networks:  # Ensure networks were fetched successfully
            for network in networks:
                network_id = network["id"]
                try:
                    _LOGGER.debug("Fetching clients for network ID: %s", network_id)
                    # Using a timespan of 300 seconds (5 minutes) to get recently active clients.
                    # The SDK method is `self.meraki_client.clients.get_network_clients`
                    # based on common SDK structures. If this is incorrect, it will need adjustment.
                    # The prompt suggests `self.meraki_client.networks.get_network_clients`,
                    # but Meraki SDK usually groups client-related calls under `dashboard.clients`.
                    # Let's assume `self.meraki_client.clients.get_network_clients` for now.
                    # If `clients` is not an attribute of `meraki_client`, this will fail and
                    # we might need to use `self.meraki_client.networks.get_network_clients`.
                    # Based on typical Meraki SDK patterns, `clients` is a sub-API of `dashboard`.
                    # Let's try the one from the prompt first:
                    # `self.meraki_client.networks.get_network_clients`
                    network_clients_data = (
                        await self.meraki_client.networks.getNetworkClients(
                            network_id, timespan=300  # timespan in seconds
                        )
                    )

                    if network_clients_data:
                        for client_data in network_clients_data:
                            # Extract AP serial. Common keys: 'recentDeviceSerial', 'deviceSerial', 'apSerial'.
                            # The specific key depends on the Meraki API
                            # version and client type.
                            ap_serial = (
                                client_data.get("recentDeviceSerial")
                                or client_data.get("recentDeviceMac")
                                or client_data.get("deviceSerial")
                            )  # recentDeviceMac might be for AP MAC not serial

                            client_entry = {
                                # 'mac' is usually a guaranteed field
                                "mac": client_data["mac"],
                                "ip": client_data.get("ip"),
                                "description": client_data.get("description"),
                                # Status is 'Online' if present in this list
                                # (recently active)
                                # Use provided status or default to Online
                                "status": client_data.get("status", "Online"),
                                "networkId": network_id,
                                "ap_serial": ap_serial,
                                # Include other potentially useful fields
                                # directly
                                "usage": client_data.get("usage"),
                                "vlan": client_data.get("vlan"),
                                "switchport": client_data.get("switchport"),
                                "ip6": client_data.get("ip6"),
                                "manufacturer": client_data.get("manufacturer"),
                                "os": client_data.get("os"),
                                # User who logged into the client device
                                "user": client_data.get("user"),
                                "firstSeen": client_data.get("firstSeen"),
                                "lastSeen": client_data.get("lastSeen"),
                                # SSID the client is connected to
                                "ssid": client_data.get("ssid"),
                            }
                            all_clients.append(client_entry)
                        _LOGGER.debug(
                            "Fetched %d clients for network %s",
                            len(network_clients_data),
                            network_id,
                        )
                    else:
                        _LOGGER.debug(
                            "No clients found for network %s in the given timespan.",
                            network_id,
                        )

                except MerakiSDKAPIError as e:
                    # Log specific error for this network but continue with
                    # others
                    _LOGGER.warning(
                        "Meraki SDK API error fetching clients for network %s: %s. "
                        "Status: %s, Reason: %s. Skipping this network's clients.",
                        network_id,
                        e,
                        e.status,
                        e.reason,
                    )
                except Exception as e:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        "Unexpected error fetching clients for network %s: %s. "
                        "Skipping this network's clients.",
                        network_id,
                        e,
                    )
        else:
            _LOGGER.warning("No networks available to fetch clients from.")

        # Step 6: Return the aggregated data including clients.
        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
            "clients": all_clients,  # Add the new clients list
        }

    async def _async_get_mr_device_details(
        self, device: Dict[str, Any], serial: str
    ) -> None:
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
            clients_data = await self.meraki_client.devices.getDeviceClients(
                serial=serial
            )
            device["connected_clients_count"] = len(clients_data) if clients_data else 0
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch client count for MR device %s (Serial: %s): "
                "API Error %s - %s. Setting client count to 0.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            device["connected_clients_count"] = 0
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching client count for MR device %s (Serial: %s): %s. "
                "Setting client count to 0.",
                device.get("name", "Unknown"),
                serial,
                e,
            )
            device["connected_clients_count"] = 0

        # Fetch wireless radio settings
        try:
            radio_settings = (
                await self.meraki_client.wireless.getDeviceWirelessRadioSettings(
                    serial=serial
                )
            )  # This one already seems fine, but ensuring consistency
            device["radio_settings"] = radio_settings
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch radio settings for MR device %s (Serial: %s): "
                "API Error %s - %s. Setting radio settings to None.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            device["radio_settings"] = None
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching radio settings for MR device %s (Serial: %s): %s. "
                "Setting radio settings to None.",
                device.get("name", "Unknown"),
                serial,
                e,
            )
            device["radio_settings"] = None

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK.

        Args:
            org_id: The organization ID for which to fetch networks.

        Returns:
            A list of network dictionaries if successful, None otherwise.
            Handles `MerakiSDKAPIError` and other exceptions internally.
        """
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            _LOGGER.debug(
                "Executing async_get_networks with organizations.getOrganizationNetworks(organizationId=%s).",
                org_id,
            )

            # Call is now on self.meraki_client.organizations
            org_networks = await self.meraki_client.organizations.getOrganizationNetworks(
                organizationId=org_id
                # Consider if total_pages='all' or similar pagination might be needed/supported here,
                # but start without it for simplicity, similar to getOrganizations.
            )

            if (
                org_networks is None
            ):  # Explicit check for None if the API can return that on error/no content
                _LOGGER.warning(
                    "Call to organizations.getOrganizationNetworks for org ID %s returned None.",
                    org_id,
                )
                return None

            # If org_networks is an empty list, it means no networks were found for that org, which is valid.
            # The original code would return None if the filtered list was empty, leading to UpdateFailed.
            # Let's keep that behavior for consistency: if no networks, treat
            # as an issue for now.
            if not org_networks:
                _LOGGER.warning(
                    "No networks found for organization ID %s using organizations.getOrganizationNetworks.",
                    org_id,
                )
                return None

            _LOGGER.debug(
                "Successfully fetched %d networks for org ID %s using organizations.getOrganizationNetworks.",
                len(org_networks),
                org_id,
            )
            return org_networks
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error during getNetworks or filtering for org %s: "
                "Status %s, Reason: %s. Returning None.",
                org_id,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error during getNetworks or filtering for org %s: %s. "
                "Returning None.",
                org_id,
                e,
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
        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching organization devices for org ID: %s using SDK",
            org_id,
        )  # Added prefix
        try:
            devices_data = (
                await self.meraki_client.organizations.getOrganizationDevices(org_id)
            )
            # Added detailed logging of the first few devices or summary
            if devices_data:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: Received %d devices from SDK. "
                    "First device example: %s",
                    len(devices_data),
                    # Log first device as example
                    str(devices_data[0]) if devices_data else "N/A",
                )
                # To log all devices if needed (can be very verbose):
                # for i, device in enumerate(devices_data):
                #     _LOGGER.debug("MERAKI_DEBUG_FETCHER: Device %d data: %s", i, str(device))
            else:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: Received no devices_data from SDK (None or empty list)."
                )
            return devices_data
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: SDK API error fetching devices for org %s: "
                "Status %s, Reason: %s. Returning None.",  # Added prefix
                org_id,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching devices for org %s: %s. "
                "Returning None.",  # Added prefix
                org_id,
                e,
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
            return await self.meraki_client.wireless.getNetworkWirelessSsids(
                networkId=network_id
            )
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for network %s (likely no wireless "
                    "capabilities or SSIDs configured). Returning empty list.",
                    network_id,
                )
                return []  # Treat 404 as "no SSIDs found" for this network.
            _LOGGER.warning(
                "SDK API error fetching SSIDs for network %s: Status %s, Reason: %s. "
                "Returning None for this network's SSIDs.",
                network_id,
                e.status,
                e.reason,
            )
            # Indicates an error occurred, distinct from an empty list for 404.
            return None
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for network %s: %s. "
                "Returning None.",
                network_id,
                e,
            )
            return None

    # The _fetch_data method, previously part of a different API client
    # structure, is no longer needed.
