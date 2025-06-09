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
from ..coordinators.meraki_device_types import (
    map_meraki_model_to_device_type,
)

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
            f"Fetching all data for organization ID: {self.org_id} using SDK"
        )

        # Step 1: Concurrently fetch foundational data
        # Networks, Devices, Device Statuses, Firmware Upgrades
        results = await asyncio.gather(
            self.async_get_networks(self.org_id),
            self.async_get_organization_devices(self.org_id),
            self.meraki_client.organizations.getOrganizationDevicesStatuses(
                organizationId=self.org_id, total_pages="all"
            ),
            self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                organizationId=self.org_id
            ),
            return_exceptions=True,  # Allows us to handle individual failures
        )

        # Unpack results and handle errors
        networks: Optional[List[Dict[str, Any]]] = None
        devices: Optional[List[Dict[str, Any]]] = None
        statuses_data: Optional[List[Dict[str, Any]]] = None
        firmware_upgrade_data_raw: Optional[List[Dict[str, Any]]] = None # Raw from API

        if isinstance(results[0], Exception):
            _LOGGER.error(f"Critical error fetching networks for org {self.org_id}: {results[0]}")
        else:
            networks = results[0]

        if isinstance(results[1], Exception):
            _LOGGER.error(f"Critical error fetching devices for org {self.org_id}: {results[1]}")
        else:
            devices = results[1]

        if isinstance(results[2], MerakiSDKAPIError):
            _LOGGER.warning(
                f"SDK API error fetching device statuses for org {self.org_id}: "
                f"Status {results[2].status}, Reason: {results[2].reason}. Device statuses may be incomplete."
            )
        elif isinstance(results[2], Exception):
            _LOGGER.exception(
                f"Unexpected error fetching device statuses for org {self.org_id}: {results[2]}. "
                "Device statuses may be incomplete."
            )
        else:
            statuses_data = results[2]

        if isinstance(results[3], MerakiSDKAPIError):
            _LOGGER.warning(
                f"SDK API error fetching firmware upgrade data for org {self.org_id}: "
                f"Status {results[3].status}, Reason: {results[3].reason}. Firmware data may be incomplete."
            )
            firmware_upgrade_data_raw = {} # Ensure it's an empty dict on error
        elif isinstance(results[3], Exception):
            _LOGGER.exception(
                f"Unexpected error fetching firmware upgrade data for org {self.org_id}: {results[3]}. "
                "Firmware data may be incomplete."
            )
            firmware_upgrade_data_raw = {} # Ensure it's an empty dict on error
        else:
            firmware_upgrade_data_raw = results[3]


        # Critical data checks
        if networks is None:
            _LOGGER.error(
                f"Could not fetch Meraki networks for org ID: {self.org_id}. Aborting update."
            )
            raise UpdateFailed(
                f"Could not fetch Meraki networks for org {self.org_id}."
            )
        if devices is None:
            _LOGGER.error(
                f"Could not fetch Meraki devices for org ID: {self.org_id}. Aborting update."
            )
            raise UpdateFailed(f"Could not fetch Meraki devices for org {self.org_id}.")

        # Step 2.1: Process Device Statuses (already fetched)
        device_statuses_map = {}
        if statuses_data:  # Check if any status data was returned and successfully processed
            for status_entry in statuses_data:
                if status_entry.get("serial"):  # Ensure serial exists.
                    device_statuses_map[status_entry["serial"]] = status_entry
        elif devices: # If devices exist but statuses_data is None/empty due to error
             _LOGGER.warning(f"Device status data was not successfully fetched for org {self.org_id}. Status-dependent info may be missing.")


        # Step 2.2: Merge Statuses into Devices (No change in this block's logic, just its position)
        if (
            devices and device_statuses_map
        ):  # Proceed if both devices and statuses data exist.
            for (
                device
            ) in devices:  # Iterate through each device from the initial fetch.
                serial = device.get("serial")
                if (
                    serial and serial in device_statuses_map
                ):  # Check if status is available for this device.
                    status_update_data = device_statuses_map[serial]
                    # Preserve original model and productType before updating.
                    # This is important because device status API might not include all details
                    # or might have different productType representations (e.g., null).
                    original_model = device.get("model", "")
                    original_product_type = device.get("productType")

                    # Merge status data into the main device dictionary.
                    # This adds new fields (like 'status', 'publicIp', etc.) and overwrites existing ones if present in status_update_data.
                    device.update(status_update_data)

                    # Post-merge checks for productType, as status data might alter it.
                    current_product_type_after_merge = device.get("productType")
                    status_provided_product_type = status_update_data.get("productType")

                    # If the status update made productType null, but we had a valid one from the initial device fetch, restore it.
                    # This handles cases where the /status endpoint might not return productType or returns it as null.
                    if (
                        current_product_type_after_merge is None
                        and original_product_type is not None
                    ):
                        # Retain this debug log as it's specific and useful for productType issues
                        _LOGGER.debug(
                            f"Restoring original productType '{original_product_type}' for device {device.get('name', 'Unknown')} (Serial: {serial}) "
                            f"as status update data had productType: {status_provided_product_type} (Type: {type(status_provided_product_type).__name__})."
                        )
                        device["productType"] = original_product_type
                    # Log if productType was unexpectedly changed by status data, but both were non-null.
                    elif (
                        original_product_type is not None
                        and status_provided_product_type is not None
                        and original_product_type != status_provided_product_type
                    ):
                        _LOGGER.warning(
                            f"productType for device {device.get('name', 'Unknown')} (Serial: {serial}) was changed from '{original_product_type}' to '{current_product_type_after_merge}' "
                            "by status update data. This is unexpected if original was valid. Using new value from status."
                        )

                    # Override productType for MX devices to ensure consistency.
                    # MX devices should always be 'appliance'. This corrects any discrepancies
                    # from the API (e.g., if /devices or /status reports it differently or as null for MX).
                    # It checks based on the original model string or the current model string.
                    if (original_model and original_model.upper().startswith("MX")) or (
                        device.get("model", "").upper().startswith("MX")
                    ):
                        if (
                            device.get("productType") != "appliance"
                        ):  # Only log if a change is made.
                            _LOGGER.debug(
                                f"Forcing productType to 'appliance' for MX device {device.get('name', 'Unknown')} (Serial: {serial}). Original model: '{original_model if original_model else device.get('model', '')}', ProductType was: '{device.get('productType')}'"
                            )
                        device["productType"] = "appliance"  # Force to 'appliance'.

                    # Log the final productType for MX devices after all modifications.
                    # This helps in debugging productType issues for MX devices.
                    if device.get("model", "").upper().startswith("MX"):
                        _LOGGER.debug(
                            f"Final productType for MX device {device.get('name', 'Unknown')} (Serial: {serial}) before leaving fetch_all_data: {device.get('productType')}"
                        )
                elif (
                    serial
                ):  # If device serial exists but no status entry was found for it.
                    _LOGGER.debug(
                        f"No specific status entry found for device {serial}. It may retain a prior status or have none."
                    )
        elif devices:  # If devices list exists but device_statuses_map is empty.
            _LOGGER.debug(
                "No device statuses were successfully mapped, skipping merge."
            )

        # Step 3: Firmware upgrade data is now `firmware_upgrade_data_raw` (already fetched)
        # The processing logic in Step 5 will use this.

        # Step 4: Fetch additional details for MR (wireless) and MX (appliance) devices.
        # This is done concurrently using asyncio.gather for efficiency.
        additional_device_detail_tasks = []
        if devices:  # Only proceed if there are devices.
            for device in devices:  # Iterate through the list of devices.
                device_model = device.get("model", "") # No .upper() here yet
                serial = device.get("serial")

                if (
                    not serial
                ):  # Skip if device serial is missing, as it's needed for API calls.
                    _LOGGER.debug(
                        f"Device {device.get('name', 'N/A')} (MAC: {device.get('mac', 'N/A')}) has no serial, skipping additional detail tasks."
                    )
                    continue

                # Determine device type using the utility function
                generic_device_type = map_meraki_model_to_device_type(device_model)
                _LOGGER.debug(f"Device {serial} (Model: {device_model}) mapped to generic type: {generic_device_type}")

                # Call _async_get_mr_device_details if it's a "Wireless" device
                if generic_device_type == "Wireless":
                    _LOGGER.debug(f"Device {serial} is Wireless, scheduling _async_get_mr_device_details.")
                    additional_device_detail_tasks.append(
                        self._async_get_mr_device_details(device, serial)
                    )
                elif device_model.upper().startswith("MX"): # Keep existing MX logic as is
                    _LOGGER.debug(f"Device {serial} is MX, scheduling MX detail tasks.")
                    additional_device_detail_tasks.append(
                        self._async_get_mx_device_uplink_settings(
                            device, self.meraki_client
                        )
                    )
                    additional_device_detail_tasks.append(
                        self._async_get_mx_lan_dns_settings(
                            device, self.meraki_client
                        )
                    )
                # Check for Camera devices (MV)
                # Use productType (more reliable) or model prefix (fallback)
                elif device.get("productType", "").lower() == "camera" or \
                     device_model.upper().startswith("MV"):
                    _LOGGER.debug(f"Device {serial} is Camera, scheduling _async_get_camera_video_settings.")
                    # Initialize rtspServerEnabled to None before task creation
                    device["rtspServerEnabled"] = None
                    additional_device_detail_tasks.append(
                        self._async_get_camera_video_settings(device, self.meraki_client)
                    )

        if additional_device_detail_tasks:  # If there are tasks to run.
            await asyncio.gather(
                *additional_device_detail_tasks
            )  # Execute all scheduled tasks concurrently.

        # Step 5: Process firmware upgrade data (now `firmware_upgrade_data_raw`) and merge into device dictionaries.
        firmware_info_map = {}
        if devices:  # Check if there are devices to process.
            if not isinstance(firmware_upgrade_data_raw, list): # Use the raw data variable
                _LOGGER.warning(
                    f"firmware_upgrade_data_raw is not a list (type: {type(firmware_upgrade_data_raw).__name__}), " # Use the raw data variable
                    f"cannot process firmware status for devices. Value: {str(firmware_upgrade_data_raw)[:200]}" # Use the raw data variable
                )
                # If data is not as expected, all devices will use default firmware status later.
            elif not firmware_upgrade_data_raw: # Use the raw data variable
                _LOGGER.debug(
                    f"firmware_upgrade_data_raw is an empty list. " # Use the raw data variable
                    f"No specific upgrade information available for org {self.org_id}."
                )
                # If list is empty, all devices will assume up-to-date status later.
            else:
                _LOGGER.debug(f"Processing firmware upgrade data (raw) to build a map for org {self.org_id}.")
                for upgrade_item in firmware_upgrade_data_raw: # Use the raw data variable
                    if not isinstance(upgrade_item, dict):
                        _LOGGER.warning(
                            f"Skipping non-dictionary item in firmware_upgrade_data_raw list: {str(upgrade_item)[:200]}" # Use the raw data variable
                        )
                        continue

                    item_serial = upgrade_item.get("serial")
                    if not item_serial:
                        _LOGGER.debug("Skipping firmware item with no serial.")
                        continue

                    # Determine firmware status for this item_serial
                    # This logic is moved from per-device iteration to here, processing each upgrade_item once.
                    # We need a way to get current_device_firmware if needed, but the goal is to pre-process.
                    # For now, we'll store what the API tells us about latest/next version.
                    # The final comparison with current_device_firmware will happen during device iteration.

                    is_item_up_to_date = False # Default for this item
                    latest_item_version = "N/A" # Default for this item

                    next_upgrade_info = upgrade_item.get("nextUpgrade")
                    if isinstance(next_upgrade_info, dict):
                        to_version_info = next_upgrade_info.get("toVersion")
                        if isinstance(to_version_info, dict):
                            latest_item_version = to_version_info.get("version", "N/A")
                            # Has a scheduled upgrade, so not up-to-date with that version yet.
                            is_item_up_to_date = False
                        else: # next_upgrade_info exists, but no toVersion
                            item_status = str(upgrade_item.get("status", "")).lower()
                            if item_status == "up-to-date":
                                is_item_up_to_date = True
                                # latest_item_version will be set based on device's current firmware later
                            elif item_status == "has-newer-stable-version":
                                is_item_up_to_date = False
                                available_versions = upgrade_item.get("availableVersions")
                                if isinstance(available_versions, list) and available_versions:
                                    latest_item_version = available_versions[0].get("version", "N/A")
                    else: # No nextUpgrade info
                        item_status = str(upgrade_item.get("status", "")).lower()
                        if item_status == "up-to-date":
                            is_item_up_to_date = True
                            # latest_item_version will be set based on device's current firmware later
                        elif upgrade_item.get("latestVersion"):
                            latest_item_version = upgrade_item.get("latestVersion")
                            # is_item_up_to_date will be determined by comparing with device's current firmware
                        elif item_status == "has-newer-stable-version": # Another explicit status
                             is_item_up_to_date = False
                             available_versions = upgrade_item.get("availableVersions")
                             if isinstance(available_versions, list) and available_versions:
                                 latest_item_version = available_versions[0].get("version", "N/A")


                    firmware_info_map[item_serial] = {
                        "api_reported_up_to_date": is_item_up_to_date,
                        "api_latest_version": latest_item_version,
                        # We also need the raw status if available, for more nuanced checks later
                        "api_status": upgrade_item.get("status", "").lower()
                    }
                    _LOGGER.debug(f"Stored firmware map info for {item_serial}: {firmware_info_map[item_serial]}")

            # Now iterate through devices and apply firmware status using the map
            for device in devices:
                device_serial = device.get("serial")
                device_model = device.get("model", "")
                current_device_firmware = device.get("firmware")

                is_up_to_date_bool = False  # Default: not up-to-date
                latest_known_version = current_device_firmware if current_device_firmware else "N/A"

                if not isinstance(firmware_upgrade_data_raw, list): # Bad data from API (use raw variable)
                    is_up_to_date_bool = False
                    # latest_known_version already set to current or N/A
                elif not firmware_upgrade_data_raw: # Empty list from API (use raw variable)
                    is_up_to_date_bool = True # Assume up-to-date
                    # latest_known_version already set to current or N/A
                elif device_serial and device_serial in firmware_info_map:
                    info = firmware_info_map[device_serial]
                    _LOGGER.debug(f"Processing device {device_serial} with firmware map info: {info}")

                    # Refined logic using map data
                    api_latest_version = info["api_latest_version"]
                    api_reported_up_to_date = info["api_reported_up_to_date"]
                    api_status = info["api_status"]

                    if api_status == "up-to-date":
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    elif api_latest_version and api_latest_version != "N/A":
                        latest_known_version = api_latest_version
                        if current_device_firmware and current_device_firmware == latest_known_version:
                            is_up_to_date_bool = True
                        else:
                            is_up_to_date_bool = False # Newer version known from API
                    elif api_reported_up_to_date: # API says up-to-date but didn't give a specific latest version
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    else: # No specific info, or API says not up-to-date
                        is_up_to_date_bool = False
                        if api_latest_version and api_latest_version != "N/A":
                             latest_known_version = api_latest_version
                        # else latest_known_version remains current device firmware or N/A

                    # Final override: if current matches latest known, it must be up-to-date
                    if current_device_firmware and current_device_firmware == latest_known_version:
                        is_up_to_date_bool = True

                else: # Device serial not in map, or map couldn't be built properly
                    _LOGGER.debug(
                        f"No specific firmware upgrade info found for device {device_serial} in map. Using defaults."
                    )
                    # Defaults are: is_up_to_date_bool = False, latest_known_version = current_device_firmware or "N/A"
                    # This is a safe assumption if no specific info is available.
                    # If firmware_upgrade_data was valid and simply no entry for this serial, it implies no upgrade scheduled for it.
                    # Consider if this should default to True if current_device_firmware is known.
                    if current_device_firmware: # If we know current, and no info otherwise, assume it's current.
                        is_up_to_date_bool = True # Or False if we want to be pessimistic
                        latest_known_version = current_device_firmware
                    else: # No current firmware, no API info for serial
                        is_up_to_date_bool = False
                        latest_known_version = "N/A"


                device["firmware_up_to_date"] = is_up_to_date_bool
                device["latest_firmware_version"] = latest_known_version
                _LOGGER.debug(
                    f"Device {device_serial} (Model: {device_model}, Current FW: {current_device_firmware}): Up-to-date: {is_up_to_date_bool}, Latest Known: {latest_known_version}"
                )
        else:  # No devices available to process.
            _LOGGER.debug(
                f"No devices available to process firmware data for org {self.org_id}."
            )

        # Step 6: Fetch SSIDs for each network.
        ssids: List[Dict[str, Any]] = []
        for (
            network
        ) in networks:  # Iterate through the list of networks obtained earlier.
            network_id: str = network["id"]  # Get network ID.
            try:
                _LOGGER.debug(f"Fetching SSIDs for network ID: {network_id}")
                ssid_data_for_network = None  # Initialize to None for this iteration.
                try:
                    # Fetch SSIDs for the current network.
                    ssid_data_for_network = await self.async_get_network_ssids(
                        network_id
                    )
                except (
                    MerakiSDKAPIError
                ) as e:  # Handle API errors during SSID fetch for a specific network.
                    _LOGGER.warning(
                        f"Error fetching SSIDs for network {network_id} was not handled by async_get_network_ssids: {e}. Status: {e.status}, Reason: {e.reason}. Skipping."
                    )
                if ssid_data_for_network:  # If SSIDs were successfully fetched.
                    for (
                        ssid_obj
                    ) in ssid_data_for_network:  # Iterate through fetched SSIDs.
                        if isinstance(ssid_obj, dict):
                            # Ensure 'networkId' is present in each SSID object.
                            # This is crucial for linking SSIDs back to their parent network.
                            if ssid_obj.get("networkId") is None:  # If missing, add it.
                                ssid_obj["networkId"] = network_id
                                _LOGGER.debug(
                                    f"Added/updated networkId '{network_id}' for SSID '{ssid_obj.get('name')}' (Number: {ssid_obj.get('number')})"
                                )
                        else:  # Log if an item in the list is not a dictionary.
                            _LOGGER.warning(
                                f"Found non-dict item in ssid_data_for_network: {ssid_obj}"
                            )
                    ssids.extend(
                        ssid_data_for_network
                    )  # Add fetched SSIDs to the main list.
                elif (
                    ssid_data_for_network is None
                ):  # If async_get_network_ssids returned None (e.g., due to error).
                    _LOGGER.info(
                        f"SSID data result was None for network {network_id}, SSIDs for this network will be skipped."
                    )
            except (
                Exception
            ) as e:  # Catch any other unexpected errors during processing of a network.
                _LOGGER.exception(
                    f"Unexpected error processing network {network_id} for SSID data: {e}. Skipping this network's SSIDs."
                )

        # Step 7: Fetch all clients across all networks.
        all_clients: List[Dict[str, Any]] = []
        if networks:  # Only proceed if networks list is available.
            for network in networks:  # Iterate through each network.
                network_id = network["id"]
                try:
                    _LOGGER.debug(f"Fetching clients for network ID: {network_id}")
                    # Fetch clients for the current network. Timespan is set to 3600 seconds (1 hour)
                    # to get a more stable count of recently active clients over a longer period,
                    # reducing short-term fluctuations compared to the previous 5-minute window.
                    network_clients_data = (
                        await self.meraki_client.networks.getNetworkClients(
                            network_id,
                            timespan=3600,  # Updated timespan to 1 hour
                        )
                    )
                    if network_clients_data:  # If clients are found.
                        for client_data in network_clients_data:  # Process each client.
                            # Attempt to get AP serial; this helps in linking clients to specific APs if needed.
                            # Different API versions/device types might use different keys for this.
                            ap_serial = (
                                client_data.get(
                                    "recentDeviceSerial"
                                )  # Primary key for AP serial.
                                or client_data.get(
                                    "recentDeviceMac"
                                )  # Fallback if serial not present.
                                or client_data.get("deviceSerial")  # Another fallback.
                            )
                            # Construct a standardized client entry dictionary.
                            client_entry = {
                                "mac": client_data["mac"],
                                "ip": client_data.get("ip"),
                                "description": client_data.get("description"),
                                "status": client_data.get(
                                    "status", "Online"
                                ),  # Default to "Online" if status missing.
                                "networkId": network_id,
                                "ap_serial": ap_serial,  # Link to network and AP.
                                # Include various other potentially useful client details.
                                "usage": client_data.get("usage"),
                                "vlan": client_data.get("vlan"),
                                "switchport": client_data.get("switchport"),
                                "ip6": client_data.get("ip6"),
                                "manufacturer": client_data.get("manufacturer"),
                                "os": client_data.get("os"),
                                "user": client_data.get("user"),
                                "firstSeen": client_data.get("firstSeen"),
                                "lastSeen": client_data.get("lastSeen"),
                                "ssid": client_data.get("ssid"),
                            }
                            all_clients.append(
                                client_entry
                            )  # Add to the list of all clients.
                        _LOGGER.debug(
                            f"Fetched {len(network_clients_data)} clients for network {network_id}"
                        )
                    else:  # No clients found for this network in the timespan.
                        _LOGGER.debug(
                            f"No clients found for network {network_id} in the given timespan."
                        )
                except (
                    MerakiSDKAPIError
                ) as e:  # Handle API errors during client fetching for a network.
                    _LOGGER.warning(
                        f"Meraki SDK API error fetching clients for network {network_id}: {e}. Status: {e.status}, Reason: {e.reason}. Skipping this network's clients."
                    )
                except Exception as e:  # Handle other unexpected errors.
                    _LOGGER.exception(
                        f"Unexpected error fetching clients for network {network_id}: {e}. Skipping this network's clients."
                    )
        else:  # No networks available to fetch clients from.
            _LOGGER.warning("No networks available to fetch clients from.")

        # Step 8: Aggregate client counts
        clients_on_ssids = 0
        clients_on_appliances = 0
        clients_on_wireless = 0

        device_serial_to_type_map = {}
        if devices:
            # Ensure 'devices' here is the comprehensive list
            for device in devices:
                serial = device.get("serial")
                model = device.get("model", "") # Ensure model is a string
                if serial and model: # model can be empty string but map_meraki_model_to_device_type should handle it
                    device_serial_to_type_map[serial] = (
                        map_meraki_model_to_device_type(model)
                    )

        # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section

        for client in all_clients:
            # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section

            # client_counted_for_wireless_or_appliance = False # Variable not used, can be removed if not intended for future use

            # Count clients on SSIDs
            if client.get("ssid"):  # Check if client is associated with an SSID
                clients_on_ssids += 1
                # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section

            # Count clients on Wireless APs or Appliances
            ap_serial = client.get("ap_serial")
            if ap_serial:
                device_type = device_serial_to_type_map.get(ap_serial)
                # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section
                if device_type == "Wireless":
                    clients_on_wireless += 1
                    # client_counted_for_wireless_or_appliance = True
                    # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section
                elif device_type == "Appliance":
                    clients_on_appliances += 1
                    # client_counted_for_wireless_or_appliance = True
                    # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section
            # else: # No specific log needed if no ap_serial, normal case for some clients
                 # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section

        _LOGGER.debug(
            f"ApiFetcher: Calculated Organization-Wide Client Counts: SSID={clients_on_ssids}, Wireless={clients_on_wireless}, Appliance={clients_on_appliances}"
        )
        _LOGGER.debug(f"Client counts for org {self.org_id}: SSID: {clients_on_ssids}, Wireless: {clients_on_wireless}, Appliance: {clients_on_appliances}")

        # Step 9: Fetch organization details to get the organization name.
        # This is used for naming the top-level organization device and related entities.
        org_details: Optional[Dict[str, Any]] = None
        org_name: Optional[str] = None
        try:
            _LOGGER.debug(f"Fetching organization details for org ID: {self.org_id}")
            org_details = await self.meraki_client.organizations.getOrganization(
                organizationId=self.org_id
            )
            if org_details and isinstance(org_details, dict):
                org_name = org_details.get("name")
                _LOGGER.debug(f"Successfully fetched organization name: {org_name} for org ID: {self.org_id}")
            else:
                _LOGGER.warning(f"Could not extract organization name. Org details: {org_details}")
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                f"SDK API error fetching organization details for org {self.org_id}: Status {e.status}, Reason: {e.reason}. Organization name will be unavailable."
            )
        except Exception as e:
            _LOGGER.exception(
                f"Unexpected error fetching organization details for org {self.org_id}: {e}. Organization name will be unavailable."
            )

        # Step 10: Return all fetched and processed data.
        # This dictionary forms the basis for what coordinators and entities will use.
        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
            "clients": all_clients,
            "clients_on_ssids": clients_on_ssids,
            "clients_on_appliances": clients_on_appliances,
            "clients_on_wireless": clients_on_wireless,
            "org_name": org_name,  # Add org_name to the returned data
        }

    async def _async_meraki_api_call(
        self, api_coro: asyncio.Task, call_description: str, return_empty_list_on_404: bool = False
    ) -> Optional[Any]:
        """Helper to make a Meraki API call and handle common exceptions."""
        _LOGGER.debug(f"Executing API call: {call_description}")
        try:
            result = await api_coro
            _LOGGER.debug(f"Successfully executed API call: {call_description}")
            return result
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                f"SDK API error during {call_description} for org {self.org_id}: Status {e.status}, Reason: {e.reason}."
            )
            if e.status == 404:
                _LOGGER.info(f"Resource not found (404) for {call_description} in org {self.org_id}.")
                if return_empty_list_on_404:
                    _LOGGER.debug(f"Returning empty list for 404 on {call_description}")
                    return []
            return None # Default return for MerakiSDKAPIError (unless 404 and return_empty_list_on_404)
        except Exception as e:
            _LOGGER.exception(
                f"Unexpected error during {call_description} for org {self.org_id}: {e}. Returning None."
            )
            return None

    async def _async_get_mr_device_details(
        self, device: Dict[str, Any], serial: str
    ) -> None:
        """Fetch and store client count and radio settings for an MR (wireless) device.

        This method updates the provided `device` dictionary in-place with
        `connected_clients_count` and `radio_settings`. It handles API errors
        gracefully by logging warnings and setting default values.

        Args:
            device: The device dictionary to update.
            serial: The serial number of the MR device.
        """
        # Ensure keys are initialized as an integer/None for all devices processed by this method
        device["connected_clients_count"] = 0
        device["radio_settings"] = None

        clients_data = await self._async_meraki_api_call(
            self.meraki_client.devices.getDeviceClients(serial=serial),
            f"getDeviceClients(serial={serial})"
        )

        if clients_data is not None:  # Will be a list, potentially empty
            device["connected_clients_count"] = len(clients_data)
            _LOGGER.debug(f"Set connected_clients_count to {len(clients_data)} for MR device {serial} (from len).")
        else:
            # API call failed (error already logged by helper), default to 0
            device["connected_clients_count"] = 0
            _LOGGER.debug(f"Clients_data was None (call failed) for MR device {serial}. connected_clients_count remains 0.")

        radio_settings_data = await self._async_meraki_api_call(
            self.meraki_client.wireless.getDeviceWirelessRadioSettings(serial=serial),
            f"getDeviceWirelessRadioSettings(serial={serial})"
        )

        if radio_settings_data is not None:
            device["radio_settings"] = radio_settings_data
            _LOGGER.debug(f"Successfully fetched radio_settings for MR device {serial}")
        else:
            # API call failed (error already logged by helper), default to None
            device["radio_settings"] = None
            _LOGGER.debug(f"Radio_settings_data was None (call failed) for MR device {serial}. radio_settings remains None.")

        _LOGGER.debug(f"Finished _async_get_mr_device_details for {serial}. Client count: {device.get('connected_clients_count')}, Radio settings type: {type(device.get('radio_settings')).__name__}")

    async def _async_get_camera_video_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Fetch and store video settings (specifically rtspServerEnabled) for a camera device.

        Updates the `device` dictionary in-place with `rtspServerEnabled`.
        Handles API errors by logging and ensuring `rtspServerEnabled` is None if fetch fails.

        Args:
            device: The camera device dictionary to update.
            client: The MerakiAPIClient instance for the API call.
        """
        serial = device.get("serial")
        # rtspServerEnabled should have been initialized to None before this task was added.

        video_settings = await self._async_meraki_api_call(
            client.camera.getDeviceCameraVideoSettings(serial=serial),
            f"getDeviceCameraVideoSettings(serial={serial})"
        )

        if video_settings is not None:
            rtsp_server_enabled = video_settings.get("rtspServerEnabled")
            device["rtspServerEnabled"] = rtsp_server_enabled
            _LOGGER.debug(
                f"Fetched video settings for camera {serial}. RTSP Enabled: {rtsp_server_enabled}"
            )
        else:
            # API call failed or returned no data (error already logged by _async_meraki_api_call)
            # device["rtspServerEnabled"] remains None (its initialized value)
            _LOGGER.warning(
                f"Could not fetch video settings for camera {serial}. rtspServerEnabled will remain None."
            )

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        call_description = f"getOrganizationNetworks(organizationId={org_id})"
        org_networks = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationNetworks(organizationId=org_id),
            call_description
        )

        if org_networks is None:  # API call failed or returned None (handled by helper)
            _LOGGER.warning(f"{call_description} returned None or failed.") # Helper already logs specifics
            return None
        if not org_networks:  # Empty list is a valid response
            _LOGGER.info(f"No networks found for organization ID {org_id}.") # Changed from warning to info
            # Depending on strictness, could return [] directly if that's preferred over None for "empty"
            return [] # Return empty list if no networks found, consistent with some other parts

        _LOGGER.debug(f"Successfully fetched {len(org_networks)} networks for org ID {org_id}.")
        return org_networks

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK."""
        call_description = f"getOrganizationDevices(organizationId={org_id})"
        devices_data = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationDevices(organizationId=org_id),
            call_description
        )

        if devices_data is None: # API call failed
            _LOGGER.warning(f"{call_description} returned None or failed.")
            return None
        if not devices_data: # Empty list
             _LOGGER.info(f"No devices found for organization ID {org_id}.")
             return []

        _LOGGER.debug(f"Received {len(devices_data)} devices from SDK for org {org_id}.")
        return devices_data

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK."""
        call_description = f"getNetworkWirelessSsids(networkId={network_id})"
        ssids_data = await self._async_meraki_api_call(
            self.meraki_client.wireless.getNetworkWirelessSsids(networkId=network_id),
            call_description,
            return_empty_list_on_404=True # Specific for SSIDs, as 404 means no wireless capability / no SSIDs
        )

        # If ssids_data is None, it means a non-404 error occurred.
        # If it's an empty list, it means either a 404 occurred and was handled, or the API returned an empty list (no SSIDs).
        if ssids_data is None:
            _LOGGER.warning(f"{call_description} failed with a non-404 error. SSIDs for this network will be unavailable.")
            return None # Critical error, not just "no SSIDs"

        # If ssids_data is an empty list (either from 404 or actual empty response), log appropriately.
        if not ssids_data:
            _LOGGER.info(f"No SSIDs found or network does not support SSIDs (network ID: {network_id}).")
            return [] # Return empty list, consistent

        return ssids_data

    async def _async_get_mx_device_uplink_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Fetch and store WAN DNS server settings from uplink configuration for an MX (appliance) device.

        This method updates the provided `device` dictionary in-place with
        `wan1_dns_servers` and `wan2_dns_servers`. It attempts to parse these
        from the device's uplink settings API response. Handles API errors
        gracefully by logging warnings and ensuring default empty lists.

        Args:
            device: The device dictionary to update.
            client: The MerakiAPIClient instance to use for the API call.
        """
        serial = device.get("serial")
        if not serial:  # Cannot proceed without a serial number.
            _LOGGER.warning(
                f"Cannot fetch uplink settings for MX device {device.get('name', 'Unknown')}: missing serial."
            )
            return

        _LOGGER.debug(
            f"Fetching uplink settings for MX device {device.get('name', 'Unknown')} (Serial: {serial})"
        )

        # Add other WANs here if needed, e.g., device["wan3_dns_servers"] = []

        uplink_settings = await self._async_meraki_api_call(
            client.appliance.getDeviceApplianceUplinksSettings(serial=serial),
            f"getDeviceApplianceUplinksSettings(serial={serial})"
        )

        try: # New try for processing, distinct from API call exception handling
            interfaces_data = uplink_settings.get("interfaces", {}) if uplink_settings else {}

            for wan_key in ["wan1", "wan2"]: # Potentially more like "cellular", etc.
                interface_specific_settings = interfaces_data.get(wan_key, {})
                dns_servers = self._extract_dns_servers_for_wan(
                    interface_name=wan_key,
                    interface_api_settings=interface_specific_settings,
                    device_global_data=device # Pass the main device dict for fallback
                )
                device[f"{wan_key}_dns_servers"] = dns_servers
                _LOGGER.debug(
                    f"Populated {wan_key}_dns_servers for {serial}: {dns_servers}"
                )

            if not uplink_settings:
                _LOGGER.debug(
                    f"Uplink settings data was None for MX device {device.get('name', 'Unknown')} (Serial: {serial}) (API call failed or returned no data). "
                    "Attempting device-level fallbacks for DNS."
                )

            # This loop will now also serve as the fallback if interfaces_data is empty due to failed API call
            for wan_key in ["wan1", "wan2"]:
                interface_specific_settings = interfaces_data.get(wan_key, {})
                dns_servers = self._extract_dns_servers_for_wan(
                    interface_name=wan_key,
                    interface_api_settings=interface_specific_settings, # This might be empty if API failed
                    device_global_data=device
                )
                # Only update if extract_dns found something, or ensure key exists
                if dns_servers:
                    device[f"{wan_key}_dns_servers"] = dns_servers
                elif f"{wan_key}_dns_servers" not in device: # Ensure key exists if nothing found
                     device[f"{wan_key}_dns_servers"] = []
                _LOGGER.debug(
                    f"Final {wan_key}_dns_servers for {serial}: {device[f'{wan_key}_dns_servers']}"
                )

        except Exception as e:  # Catch errors from processing the uplink_settings data itself
            _LOGGER.exception(
                f"Unexpected error processing uplink settings for MX device {device.get('name', 'Unknown')} (Serial: {serial}): {e}. "
                "Ensuring DNS keys exist with fallback."
            )
            for wan_key in ["wan1", "wan2"]: # Ensure keys exist even if processing failed
                if f"{wan_key}_dns_servers" not in device:
                    # Attempt one last fallback if processing failed badly
                    device[f"{wan_key}_dns_servers"] = self._extract_dns_servers_for_wan(
                        interface_name=wan_key,
                        interface_api_settings={}, # No API settings to process
                        device_global_data=device,
                        force_device_fallback_check=True # Force check of device global data
                    )
                    _LOGGER.debug(
                        f"Ensured {wan_key}_dns_servers for {serial} after processing error: {device[f'{wan_key}_dns_servers']}"
                    )

    def _extract_dns_servers_for_wan(
        self, interface_name: str, interface_api_settings: Dict[str, Any], device_global_data: Dict[str, Any], force_device_fallback_check: bool = False
    ) -> List[str]:
        """Helper to extract DNS servers for a specific WAN interface using multiple fallbacks."""
        current_wan_dns_ips = []

        # 1. Primary: 'svis' -> 'ipv4' -> 'nameservers' (from specific interface API settings)
        if not force_device_fallback_check: # Only try API data if not forced to skip to device global
            svis_data = interface_api_settings.get("svis")
            if isinstance(svis_data, dict):
                ipv4_data = svis_data.get("ipv4")
                if isinstance(ipv4_data, dict):
                    nameservers_list = ipv4_data.get("nameservers")
                    if isinstance(nameservers_list, list):
                        for ns_entry in nameservers_list:
                            if isinstance(ns_entry, dict) and isinstance(ns_entry.get("addresses"), list):
                                for ip_addr in ns_entry.get("addresses", []):
                                    if isinstance(ip_addr, str) and ip_addr not in current_wan_dns_ips:
                                        current_wan_dns_ips.append(ip_addr)

            if current_wan_dns_ips: # Found via primary API method
                return current_wan_dns_ips

            # 2. Fallback: 'dnsServers' directly under interface_settings (from specific interface API settings)
            dns_servers_field = interface_api_settings.get("dnsServers")
            if isinstance(dns_servers_field, list):
                for dns_entry in dns_servers_field:
                    if isinstance(dns_entry, str) and ( "." in dns_entry or ":" in dns_entry):
                        if dns_entry not in current_wan_dns_ips:
                            current_wan_dns_ips.append(dns_entry)
            elif isinstance(dns_servers_field, str) and ("." in dns_servers_field or ":" in dns_servers_field):
                if dns_servers_field not in current_wan_dns_ips:
                    current_wan_dns_ips.append(dns_servers_field)

            if current_wan_dns_ips: # Found via secondary API method
                return current_wan_dns_ips

        # 3. Second Fallback: Device-level fields like 'wan1PrimaryDns' (from global device data)
        # This part is crucial if API data is missing/empty or if force_device_fallback_check is True
        primary_dns_key = f"{interface_name}PrimaryDns"
        secondary_dns_key = f"{interface_name}SecondaryDns"

        primary_dns = device_global_data.get(primary_dns_key)
        if primary_dns and isinstance(primary_dns, str) and primary_dns not in current_wan_dns_ips:
            current_wan_dns_ips.append(primary_dns)

        secondary_dns = device_global_data.get(secondary_dns_key)
        if secondary_dns and isinstance(secondary_dns, str) and secondary_dns not in current_wan_dns_ips:
            current_wan_dns_ips.append(secondary_dns)

        return current_wan_dns_ips

    async def _async_get_mx_lan_dns_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Fetch and store LAN DNS settings from VLAN configurations for an MX (appliance) device.

        This method updates the provided `device` dictionary in-place with
        `lan_dns_settings`, a dictionary mapping VLAN names/IDs to their
        DNS configurations (e.g., "google_dns", "opendns", or a list of custom IPs).
        Handles API errors gracefully.

        Args:
            device: The device dictionary to update.
            client: The MerakiAPIClient instance to use for the API call.
        """
        network_id = device.get(
            "networkId"
        )  # Network ID is required to fetch VLANs for the network the MX is in.
        serial = device.get("serial", "N/A")  # For logging purposes.
        device_name = device.get("name", "Unknown")  # For logging purposes.

        if not network_id:  # Cannot proceed without network ID.
            _LOGGER.debug(
                f"Cannot fetch LAN DNS settings for MX device {device_name} (Serial: {serial}): missing networkId."
            )
            device["lan_dns_settings"] = (
                {}
            )  # Ensure the key exists in the device dict, even if empty.
            return

        _LOGGER.debug(
            f"Fetching LAN DNS (VLAN settings) for MX device {device_name} (Serial: {serial}, Network: {network_id})"
        )

        lan_dns_by_vlan: Dict[str, Any] = (
            {}
        )  # Dictionary to store DNS settings per VLAN.
        vlan_list_to_iterate: List[Dict[str, Any]] = (
            []
        )  # List to hold VLAN data from API for consistent processing.
        try:
            vlan_settings_response = await self._async_meraki_api_call(
                client.appliance.getNetworkApplianceVlansSettings(networkId=network_id),
                f"getNetworkApplianceVlansSettings(networkId={network_id})",
                return_empty_list_on_404=True # 404 on VLANs might mean no VLANs configured / not an appliance
            )

            # Standardize response to be a list for consistent processing logic.
            if isinstance(
                vlan_settings_response, dict
            ):  # If API returns a single VLAN object.
                _LOGGER.debug(
                    f"Received single dictionary for VLAN settings for network {network_id} (Serial: {serial}). Wrapping in a list."
                )
                vlan_list_to_iterate = [vlan_settings_response]  # Wrap in a list.
            elif isinstance(
                vlan_settings_response, list
            ):  # If API returns a list of VLANs.
                vlan_list_to_iterate = vlan_settings_response
            elif (
                vlan_settings_response is None
            ):  # If no VLANs are configured or endpoint not applicable (e.g. device not an MX).
                _LOGGER.debug(
                    f"No VLANs configured or endpoint not applicable for network {network_id} (Serial: {serial}) (response is None)."
                )
                # vlan_list_to_iterate remains empty, which is handled gracefully below.
            else:  # Unexpected response type from the API.
                _LOGGER.warning(
                    f"Unexpected response type for VLAN settings for network {network_id} (Serial: {serial}): {type(vlan_settings_response).__name__}. Expected list or dict."
                )
                # vlan_list_to_iterate remains empty.

            if vlan_list_to_iterate:  # If there are VLANs to process.
                _LOGGER.debug(
                    f"Processing {len(vlan_list_to_iterate)} VLAN entries for network {network_id}."
                )
                for (
                    vlan_data
                ) in vlan_list_to_iterate:  # Iterate through each VLAN's data.
                    if not isinstance(vlan_data, dict):  # Skip malformed entries.
                        _LOGGER.warning(
                            f"Skipping non-dictionary item in VLAN settings list for network {network_id}: {vlan_data}"
                        )
                        continue

                    vlan_id = vlan_data.get("id")  # ID of the VLAN, e.g., "10".
                    vlan_name = vlan_data.get(
                        "name", "Unnamed VLAN"
                    )  # Name of the VLAN, e.g., "Data VLAN".
                    # 'dnsNameservers' indicates how DNS is configured for this VLAN:
                    # Possible values: "google_dns", "opendns", "custom_servers", "upstream_dns".
                    dns_nameservers_setting = vlan_data.get("dnsNameservers")
                    # 'customDnsServers' is a list of IPs, used if dnsNameservers_setting == "custom_servers".
                    custom_dns_servers = vlan_data.get(
                        "customDnsServers", []
                    )  # Default to empty list.
                    vlan_key = f"VLAN {vlan_id} ({vlan_name})"  # Key for storing in our result dict, e.g., "VLAN 10 (Data VLAN)".

                    if (
                        dns_nameservers_setting == "custom_servers"
                    ):  # If VLAN uses custom DNS servers.
                        if custom_dns_servers:  # If custom IPs are provided.
                            lan_dns_by_vlan[vlan_key] = custom_dns_servers
                            _LOGGER.debug(
                                f"VLAN {vlan_key} on {serial} using custom DNS: {custom_dns_servers}"
                            )
                        else:  # If set to "custom_servers" but no IPs are listed.
                            lan_dns_by_vlan[vlan_key] = []  # Store as empty list.
                            _LOGGER.debug(
                                f"VLAN {vlan_key} on {serial} set to 'custom_servers' but no IPs provided."
                            )
                    elif (
                        dns_nameservers_setting
                    ):  # If not "custom_servers", store the setting string itself (e.g., "google_dns").
                        lan_dns_by_vlan[vlan_key] = dns_nameservers_setting
                        _LOGGER.debug(
                            f"VLAN {vlan_key} on {serial} using preset DNS: {dns_nameservers_setting}"
                        )
                    else:  # If no specific DNS setting ('dnsNameservers') found for the VLAN.
                        lan_dns_by_vlan[vlan_key] = (
                            "Not configured"  # Indicate not configured.
                        )
                        _LOGGER.debug(
                            f"VLAN {vlan_key} on {serial} has no explicit DNS configuration."
                        )
            # If vlan_list_to_iterate is empty (e.g., from None response or unexpected type), this loop is skipped.

        except MerakiSDKAPIError as e:
            # Error already logged by _async_meraki_api_call if vlan_settings_response is None due to API error.
            # If it's None (non-404 error) or an empty list (e.g. from 404 handled by helper), lan_dns_by_vlan remains {}.
            if vlan_settings_response is None : # Indicates a non-404 error from helper
                 _LOGGER.warning(f"LAN DNS settings could not be fetched for MX device {device_name} (Serial: {serial}, Network: {network_id}).")

        except Exception as e: # Should be rare if helper catches most things
            _LOGGER.exception(
                f"Unexpected error structure in _async_get_mx_lan_dns_settings for {device_name} (Serial: {serial}, Network: {network_id}): {e}."
            )

        # Store the collected LAN DNS settings in the main device dictionary.
        device["lan_dns_settings"] = lan_dns_by_vlan
        _LOGGER.debug(
            f"Final LAN DNS settings for {device_name} (Serial: {serial}): {lan_dns_by_vlan}"
        )
