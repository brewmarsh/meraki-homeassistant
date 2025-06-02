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
                            # Store the entire status dictionary, not just the status string
                            device_statuses_map[status_entry["serial"]] = status_entry
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
                    status_update_data = device_statuses_map[serial]
                    original_product_type = device.get("productType") # Store original productType

                    # Perform the update
                    device.update(status_update_data)

                    # Check if productType was overwritten to None, and restore if necessary
                    current_product_type_after_merge = device.get("productType")
                    status_provided_product_type = status_update_data.get("productType") # What status data tried to set

                    if current_product_type_after_merge is None and original_product_type is not None:
                        _LOGGER.debug(
                            "MERAKI_DEBUG_FETCHER: Restoring original productType '%s' for device %s (Serial: %s) "
                            "as status update data had productType: %s (Type: %s).",
                            original_product_type,
                            device.get('name', 'Unknown'),
                            serial,
                            status_provided_product_type,
                            type(status_provided_product_type).__name__
                        )
                        device["productType"] = original_product_type
                    elif original_product_type is not None and \
                         status_provided_product_type is not None and \
                         original_product_type != status_provided_product_type:
                        _LOGGER.warning(
                            "MERAKI_DEBUG_FETCHER: productType for device %s (Serial: %s) was changed from '%s' to '%s' "
                            "by status update data. This is unexpected if original was valid. Using new value from status.",
                            device.get('name', 'Unknown'),
                            serial,
                            original_product_type,
                            current_product_type_after_merge
                        )
                    # If original_product_type was None and status provided one, that's fine (newly added info)
                    # If both are None, it remains None.
                    # If they are the same non-None value, also fine.
                elif serial:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: No specific status entry found for device %s. It may retain a prior status or have none.",
                        serial,
                    )
        elif devices:
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: No device statuses were successfully mapped, skipping merge."
            )
        
        # Log a sample of a few complete device entries after status merge
        if devices:
            # DEBUG: Verbose full device_info log for sample devices - for i, device_sample in enumerate(devices[:2]):
            #    _LOGGER.debug(
            #        "MERAKI_DEBUG_FETCHER: Sample device entry %d after status merge: %s",
            #        i,
            #        device_sample
            #    )
            pass # Keep the if block structure if other summary logs might be added later

        # Initialize for MX-specific data
        # device_uplink_settings_map = {} # This will be populated by helper tasks directly into device dict
        firmware_upgrade_data = {}

        # Step 2b: Fetch Firmware Upgrade Availability (once per organization)
        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching firmware upgrade data for org ID: %s",
            self.org_id,
        )
        try:
            firmware_upgrade_data = await self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                organizationId=self.org_id
            )
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: Successfully fetched firmware upgrade data. Data: %s",
                firmware_upgrade_data, # Be mindful of logging potentially large/sensitive data
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: SDK API error fetching firmware upgrade data for org %s: "
                "Status %s, Reason: %s. Firmware data may be incomplete.",
                self.org_id,
                e.status,
                e.reason,
            )
            firmware_upgrade_data = {} # Ensure it's an empty dict on failure
        except Exception as e:
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching firmware upgrade data for org %s: %s. "
                "Firmware data may be incomplete.",
                self.org_id,
                e,
            )
            firmware_upgrade_data = {} # Ensure it's an empty dict on failure


        # Step 2c: Fetch additional details for MR and MX devices.
        # This involves creating a list of asynchronous tasks.
        additional_device_detail_tasks = []
        # Ensure devices is not None before iterating
        if devices:
            for device in devices:
                device_model_upper = device.get("model", "").upper()
                serial = device.get("serial") # Get serial once

                if not serial: # Skip if no serial, critical for API calls
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Device %s (MAC: %s) has no serial, skipping additional detail tasks.",
                        device.get("name", "N/A"),
                        device.get("mac", "N/A"),
                    )
                    continue

                if device_model_upper.startswith("MR"):
                    additional_device_detail_tasks.append(
                        self._async_get_mr_device_details(device, serial)
                    )
                elif device_model_upper.startswith("MX"):
                    additional_device_detail_tasks.append(
                        self._async_get_mx_device_uplink_settings(device, self.meraki_client) # Pass client here
                    )
                    # Add task for LAN DNS settings for MX devices
                    additional_device_detail_tasks.append(
                        self._async_get_mx_lan_dns_settings(device, self.meraki_client)
                    )
                    # Note: _async_get_mx_device_uplink_settings will modify 'device' in place

        if additional_device_detail_tasks:
            await asyncio.gather(*additional_device_detail_tasks)
            # Results of these tasks (client counts, radio settings, MX uplink settings)
            # are directly updated in the respective device dictionaries within the `devices` list.

        # Step 3: Process Firmware Data and Merge into Devices
        if devices: # Only process if there are devices
            if not isinstance(firmware_upgrade_data, list):
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: firmware_upgrade_data is not a list (type: %s), "
                    "cannot process firmware status for devices. Value: %s",
                    type(firmware_upgrade_data).__name__,
                    str(firmware_upgrade_data)[:200] # Log a snippet
                )
                # Set defaults for all devices as firmware data is unusable
                for device in devices:
                    device["firmware_up_to_date"] = False
                    device["latest_firmware_version"] = device.get("firmware", "N/A")
            elif not firmware_upgrade_data:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: firmware_upgrade_data is an empty list. "
                    "No specific upgrade information available."
                )
                for device in devices:
                    device["firmware_up_to_date"] = True # Assuming if no upgrades listed, current is considered latest
                    device["latest_firmware_version"] = device.get("firmware", "N/A")
            else:
                _LOGGER.debug("MERAKI_DEBUG_FETCHER: Starting to process firmware data list for devices.")
                if _LOGGER.isEnabledFor(logging.DEBUG): # Log sample only if debug is enabled
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Sample firmware_upgrade_data item: %s",
                        str(firmware_upgrade_data[0])[:300] # Log a snippet of the first item
                    )

                for device in devices:
                    device_serial = device.get("serial")
                    device_model = device.get("model", "")
                    current_device_firmware = device.get("firmware")

                    # Initialize defaults for this device
                    is_up_to_date_bool = False # Default to False, assuming an upgrade might be available
                    # Default latest version to current, can be overridden by specific upgrade info
                    latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    
                    found_specific_info_for_device = False

                    for upgrade_item in firmware_upgrade_data:
                        if not isinstance(upgrade_item, dict):
                            _LOGGER.warning(
                                "MERAKI_DEBUG_FETCHER: Skipping non-dictionary item in firmware_upgrade_data list: %s",
                                str(upgrade_item)[:200]
                            )
                            continue

                        item_serial = upgrade_item.get("serial")
                        
                        # Most specific match: by serial number
                        if item_serial and item_serial == device_serial:
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: Found firmware info by serial for %s", device_serial)
                            # Example structure: {"serial": "X", "deviceModel": "MXY", "firmware": "current", "status": "up-to-date" / "available"}
                            # Or: {"serial": "X", ..., "nextUpgrade": {"toVersion": {"version": "1.2.4"}}}
                            
                            next_upgrade_info = upgrade_item.get("nextUpgrade")
                            if isinstance(next_upgrade_info, dict):
                                to_version_info = next_upgrade_info.get("toVersion")
                                if isinstance(to_version_info, dict):
                                    latest_known_version = to_version_info.get("version", latest_known_version)
                                    # If nextUpgrade exists, it implies current is not the latest targeted one
                                    is_up_to_date_bool = False 
                                else: # No specific toVersion, check overall status if available
                                    item_status = str(upgrade_item.get("status", "")).lower()
                                    # Common statuses: 'up-to-date', 'has-newer-stable-version', 'beta-available'
                                    if item_status == "up-to-date":
                                        is_up_to_date_bool = True
                                        # If status is up-to-date, then current firmware is the latest known for this device
                                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                                    elif item_status == "has-newer-stable-version":
                                        is_up_to_date_bool = False
                                        # latest_known_version might not be in this specific item if only status is given
                                        # Need to check 'availableVersions' or 'latestVersion' if present
                                        available_versions = upgrade_item.get("availableVersions")
                                        if isinstance(available_versions, list) and available_versions:
                                            # Assuming the first one is the most relevant or latest stable
                                            # This part is speculative: API might sort them or provide 'latestStable'
                                            latest_known_version = available_versions[0].get("version", latest_known_version)

                            else: # No nextUpgrade, check general status or version fields
                                item_status = str(upgrade_item.get("status", "")).lower()
                                if item_status == "up-to-date":
                                    is_up_to_date_bool = True
                                    latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                                elif upgrade_item.get("latestVersion"): # Check for a direct latest version field
                                     latest_known_version = upgrade_item.get("latestVersion")

                            # If after all checks, latest_known_version is still the current one, then it's up to date
                            if current_device_firmware and current_device_firmware == latest_known_version:
                                is_up_to_date_bool = True
                                
                            found_specific_info_for_device = True
                            break # Found device-specific info by serial

                    # If no specific serial match was found, we can't reliably determine firmware status
                    # from a generic list unless it provides model-based latest versions.
                    # The current loop structure prioritizes serial. If firmware_upgrade_data
                    # also contains general model availability, that logic would be more complex
                    # and would need to run if not found_specific_info_for_device.
                    # For now, if no serial match, is_up_to_date_bool remains its default (False, or True if list was empty)
                    # and latest_known_version remains current device firmware.

                    if not found_specific_info_for_device and not firmware_upgrade_data: # Empty list implies up-to-date
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    elif not found_specific_info_for_device:
                        # Could try a model-based lookup here if the API provides such entries in the list
                        # For now, we assume if no serial match, we don't have enough info from this list structure
                        # to definitively say it's NOT up-to-date, unless a global "latest for model X" is found.
                        # This part remains speculative. A simple approach: if no specific info, assume current is what we know.
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: No specific firmware upgrade info found for device %s by serial.", device_serial)
                        # Heuristic: if we haven't found a newer version, and current firmware is known, assume up-to-date relative to available data.
                        if current_device_firmware:
                            is_up_to_date_bool = (current_device_firmware == latest_known_version)


                    device["firmware_up_to_date"] = is_up_to_date_bool
                    device["latest_firmware_version"] = latest_known_version
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Device %s (Model: %s, Current FW: %s): Up-to-date: %s, Latest Known: %s",
                        device_serial,
                        device_model,
                        current_device_firmware,
                        is_up_to_date_bool,
                        latest_known_version,
                    )
        else: # No devices
            _LOGGER.debug("MERAKI_DEBUG_FETCHER: No devices available to process firmware data for.")
            # firmware_upgrade_data is not processed if there are no devices.

        ssids: List[Dict[str, Any]] = []
        # The `network_clients_data` dictionary is no longer needed here as client counting
        # for MR devices is handled by `_async_get_mr_device_details`.
        # If a list of all clients per network was needed elsewhere, it would
        # be collected here.

        # Step 4: Iterate through each network to fetch its SSIDs.
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
                    for ssid_obj in ssid_data_for_network:
                        # Ensure networkId is present in each SSID object.
                        # The SDK should ideally include this, but if not, or if it's under a different key,
                        # this ensures our data structure is consistent.
                        # We are adding it if it's not present or if it's None,
                        # as the logs showed networkId: None.
                        if isinstance(ssid_obj, dict):
                            if ssid_obj.get("networkId") is None: # Check if None or missing
                                ssid_obj["networkId"] = network_id
                                _LOGGER.debug(f"Added/updated networkId '{network_id}' for SSID '{ssid_obj.get('name')}' (Number: {ssid_obj.get('number')})")
                        else:
                            _LOGGER.warning(f"Found non-dict item in ssid_data_for_network: {ssid_obj}")
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
                # DEBUG: Verbose log for first device example - _LOGGER.debug(
                #    "MERAKI_DEBUG_FETCHER: Received %d devices from SDK. "
                #    "First device example: %s",
                #    len(devices_data),
                #    str(devices_data[0]) if devices_data else "N/A",
                # )
                _LOGGER.debug( # Keep a less verbose summary
                    "MERAKI_DEBUG_FETCHER: Received %d devices from SDK.",
                    len(devices_data)
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


    async def _async_get_mx_device_uplink_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Asynchronously fetch and store uplink settings for an MX device.

        This helper method updates the provided `device` dictionary in-place with
        `wan1_dns_servers` and `wan2_dns_servers`. It handles API errors
        gracefully by logging them.

        Args:
            device: The dictionary representing the MX device to update.
            client: The MerakiAPIClient instance.
        """
        serial = device.get("serial")
        if not serial:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: Cannot fetch uplink settings for MX device %s: missing serial.",
                device.get("name", "Unknown"),
            )
            return

        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching uplink settings for MX device %s (Serial: %s)",
            device.get("name", "Unknown"),
            serial,
        )
        try:
            # Ensure the client object is correctly passed and used.
            # The method is client.appliance.getDeviceApplianceUplinksSettings
            uplink_settings = await client.appliance.getDeviceApplianceUplinksSettings(
                serial=serial
            )
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: Raw uplink settings for %s: %s",
                serial,
                uplink_settings, # Be cautious logging entire complex objects
            )

            # Initialize DNS server lists for the device to ensure they always exist
            device["wan1_dns_servers"] = []
            device["wan2_dns_servers"] = []


    async def _async_get_mx_lan_dns_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Asynchronously fetch and store LAN DNS settings for an MX device's VLANs."""
        network_id = device.get("networkId")
        serial = device.get("serial", "N/A") # For logging
        device_name = device.get("name", "Unknown")

        if not network_id:
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: Cannot fetch LAN DNS settings for MX device %s (Serial: %s): missing networkId.",
                device_name,
                serial,
            )
            device["lan_dns_settings"] = {} # Ensure key exists
            return

        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching LAN DNS (VLAN settings) for MX device %s (Serial: %s, Network: %s)",
            device_name,
            serial,
            network_id,
        )
        
        lan_dns_by_vlan: Dict[str, Any] = {}
        try:
            vlan_settings_list = await client.appliance.getNetworkApplianceVlansSettings(
                networkId=network_id
            )

            if vlan_settings_list and isinstance(vlan_settings_list, list):
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: Received %d VLAN entries for network %s.",
                    len(vlan_settings_list),
                    network_id
                )
                for vlan_data in vlan_settings_list:
                    if not isinstance(vlan_data, dict):
                        _LOGGER.warning("Skipping non-dictionary item in VLAN settings list for network %s: %s", network_id, vlan_data)
                        continue
                    
                    vlan_id = vlan_data.get("id")
                    vlan_name = vlan_data.get("name", "Unnamed VLAN")
                    dns_nameservers_setting = vlan_data.get("dnsNameservers")
                    custom_dns_servers = vlan_data.get("customDnsServers", [])

                    vlan_key = f"VLAN {vlan_id} ({vlan_name})"

                    if dns_nameservers_setting == "custom_servers":
                        if custom_dns_servers:
                            lan_dns_by_vlan[vlan_key] = custom_dns_servers
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s using custom DNS: %s", vlan_key, serial, custom_dns_servers)
                        else:
                            lan_dns_by_vlan[vlan_key] = [] # Custom selected but none provided
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s set to 'custom_servers' but no IPs provided.", vlan_key, serial)
                    elif dns_nameservers_setting:
                        lan_dns_by_vlan[vlan_key] = dns_nameservers_setting # e.g., "google_dns", "opendns", "upstream_dns"
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s using preset DNS: %s", vlan_key, serial, dns_nameservers_setting)
                    else:
                        lan_dns_by_vlan[vlan_key] = "Not configured" # Or empty list, depending on preference
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s has no explicit DNS configuration.", vlan_key, serial)
            elif vlan_settings_list is None: # Explicit None means no VLANs or not applicable.
                 _LOGGER.debug("MERAKI_DEBUG_FETCHER: No VLANs configured or endpoint not applicable for network %s (Serial: %s).", network_id, serial)
            else: # Unexpected response type
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: Unexpected response type for VLAN settings for network %s (Serial: %s): %s",
                    network_id, serial, type(vlan_settings_list).__name__
                )

        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: No VLAN settings found for network %s (Serial: %s) (404 Error). "
                    "This may be normal if no VLANs are configured or device is not an appliance.",
                    network_id,
                    serial,
                )
            else:
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: Failed to fetch LAN DNS settings for MX device %s (Serial: %s, Network: %s): "
                    "API Error %s - %s. LAN DNS settings will be unavailable.",
                    device_name,
                    serial,
                    network_id,
                    e.status,
                    e.reason,
                )
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching LAN DNS settings for MX device %s (Serial: %s, Network: %s): %s. "
                "LAN DNS settings will be unavailable.",
                device_name,
                serial,
                network_id,
                e,
            )
        
        device["lan_dns_settings"] = lan_dns_by_vlan
        _LOGGER.debug("MERAKI_DEBUG_FETCHER: Final LAN DNS settings for %s (Serial: %s): %s", device_name, serial, lan_dns_by_vlan)
            # Add other WANs here if needed, e.g., device["wan3_dns_servers"] = []

            if uplink_settings:
                interfaces = uplink_settings.get("interfaces", {})
                wan_interface_keys = ["wan1", "wan2"] # Extend if handling more (e.g., "wan3", "cellular")

                for interface_name in wan_interface_keys:
                    current_wan_dns_ips = []
                    interface_settings = interfaces.get(interface_name, {})

                    if interface_settings:
                        # Path 1: New SVI structure (e.g., MX19+ firmware)
                        # interfaces.<wanX>.svis.ipv4.nameservers (list of objects)
                        # Each object: {'addresses': ['1.1.1.1', '2.2.2.2']}
                        svis_data = interface_settings.get("svis")
                        if isinstance(svis_data, dict): # svis is usually a dict, not list. If list, code needs change.
                            ipv4_data = svis_data.get("ipv4")
                            if isinstance(ipv4_data, dict):
                                nameservers_list = ipv4_data.get("nameservers")
                                if isinstance(nameservers_list, list):
                                    for ns_entry in nameservers_list:
                                        if isinstance(ns_entry, dict) and isinstance(ns_entry.get("addresses"), list):
                                            for ip_addr in ns_entry.get("addresses", []):
                                                if isinstance(ip_addr, str) and ip_addr not in current_wan_dns_ips:
                                                    current_wan_dns_ips.append(ip_addr)
                        
                        # Path 2: Older "dnsServers" field (list of strings, can be "google_dns" or IPs)
                        # We only add if they appear to be actual IPs and aren't already captured.
                        # This path is less prioritized if SVI path yielded results.
                        if not current_wan_dns_ips: # Only if SVI path didn't yield IPs
                            dns_servers_field = interface_settings.get("dnsServers") # This was the old logic path
                            if isinstance(dns_servers_field, list):
                                for dns_entry in dns_servers_field:
                                    if isinstance(dns_entry, str):
                                        # Basic IP validation or check against known non-IP strings
                                        if '.' in dns_entry or ':' in dns_entry: # Simple check for IP format
                                            if dns_entry not in current_wan_dns_ips:
                                                current_wan_dns_ips.append(dns_entry)
                            elif isinstance(dns_servers_field, str): # Handle single string
                                if '.' in dns_servers_field or ':' in dns_servers_field:
                                     if dns_servers_field not in current_wan_dns_ips:
                                        current_wan_dns_ips.append(dns_servers_field)


                    # Path 3: Fallback to device-level primary/secondary DNS if list is still empty
                    if not current_wan_dns_ips:
                        primary_dns_key = f"{interface_name}PrimaryDns" # e.g., "wan1PrimaryDns"
                        secondary_dns_key = f"{interface_name}SecondaryDns" # e.g., "wan1SecondaryDns"
                        
                        primary_dns = device.get(primary_dns_key)
                        if primary_dns and isinstance(primary_dns, str) and primary_dns not in current_wan_dns_ips:
                            current_wan_dns_ips.append(primary_dns)
                        
                        secondary_dns = device.get(secondary_dns_key)
                        if secondary_dns and isinstance(secondary_dns, str) and secondary_dns not in current_wan_dns_ips:
                            current_wan_dns_ips.append(secondary_dns)
                    
                    device[f"{interface_name}_dns_servers"] = current_wan_dns_ips
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Populated %s_dns_servers for %s: %s",
                        interface_name,
                        serial,
                        device[f"{interface_name}_dns_servers"]
                    )

            else: # No uplink_settings data
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: No uplink settings data returned for MX device %s (Serial: %s). "
                    "DNS server lists will remain default (empty or from device status).",
                    device.get("name", "Unknown"),
                    serial,
                )
                # Ensure keys exist (already done at start of method)

        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: Failed to fetch uplink settings for MX device %s (Serial: %s): "
                "API Error %s - %s. DNS server info will be unavailable.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            device["wan1_dns_servers"] = []
            device["wan2_dns_servers"] = []
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching uplink settings for MX device %s (Serial: %s): %s. "
                "DNS server info will be unavailable.",
                device.get("name", "Unknown"),
                serial,
                e,
            )
            device["wan1_dns_servers"] = []
            device["wan2_dns_servers"] = []
