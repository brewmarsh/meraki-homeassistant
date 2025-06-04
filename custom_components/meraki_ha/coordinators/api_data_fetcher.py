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
            "Fetching all data for organization ID: %s using SDK", self.org_id
        )

        # Step 1: Fetch all networks for the organization.
        # `async_get_networks` handles its own exceptions and returns None on failure.
        networks: Optional[List[Dict[str, Any]]] = None
        try:
            # Attempt to fetch all networks for the organization. This is a foundational step,
            # as networks are containers for devices and SSIDs.
            networks = await self.async_get_networks(self.org_id)
        except (
            MerakiSDKAPIError
        ) as e:  # Should be caught by async_get_networks, but as a safeguard.
            # This catch block is a defensive measure. Ideally, async_get_networks
            # should internally handle API errors and return None, which is checked below.
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
            # Fetch all devices associated with the organization. This list will be
            # enriched with status, tags, and device-specific details later.
            devices = await self.async_get_organization_devices(self.org_id)
        except MerakiSDKAPIError as e:  # Safeguard.
            # Similar to network fetching, async_get_organization_devices should handle
            # its errors. This is a fallback.
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
        device_statuses_map = (
            {}
        )  # Initialize a map to store device statuses keyed by serial.
        if devices:  # Only fetch statuses if we have a list of devices.
            try:
                # Retrieve status for all devices in the organization.
                # 'total_pages="all"' ensures pagination is handled by the SDK.
                statuses_data = await self.meraki_client.organizations.getOrganizationDevicesStatuses(
                    organizationId=self.org_id, total_pages="all"
                )
                if statuses_data:  # Check if any status data was returned.
                    # Populate the map with statuses, using device serial as the key.
                    for status_entry in statuses_data:
                        if status_entry.get("serial"):  # Ensure serial exists.
                            device_statuses_map[status_entry["serial"]] = status_entry
                # else: # No specific log needed if no data, handled by later checks
            except MerakiSDKAPIError as e:
                _LOGGER.warning(
                    "SDK API error fetching device statuses for org %s: "
                    "Status %s, Reason: %s. Device statuses may be incomplete.",
                    self.org_id,
                    e.status,
                    e.reason,
                )
            except Exception as e:
                _LOGGER.exception(
                    "Unexpected error fetching device statuses for org %s: %s. "
                    "Device statuses may be incomplete.",
                    self.org_id,
                    e,
                )

        # Step 2.2: Merge Statuses into Devices
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
                            "Restoring original productType '%s' for device %s (Serial: %s) "
                            "as status update data had productType: %s (Type: %s).",
                            original_product_type,
                            device.get("name", "Unknown"),
                            serial,
                            status_provided_product_type,
                            type(status_provided_product_type).__name__,
                        )
                        device["productType"] = original_product_type
                    # Log if productType was unexpectedly changed by status data, but both were non-null.
                    elif (
                        original_product_type is not None
                        and status_provided_product_type is not None
                        and original_product_type != status_provided_product_type
                    ):
                        _LOGGER.warning(
                            "productType for device %s (Serial: %s) was changed from '%s' to '%s' "
                            "by status update data. This is unexpected if original was valid. Using new value from status.",
                            device.get("name", "Unknown"),
                            serial,
                            original_product_type,
                            current_product_type_after_merge,
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
                                "Forcing productType to 'appliance' for MX device %s (Serial: %s). Original model: '%s', ProductType was: '%s'",
                                device.get("name", "Unknown"),
                                serial,
                                (
                                    original_model
                                    if original_model
                                    else device.get("model", "")
                                ),  # Log the model used for the check
                                device.get(
                                    "productType"
                                ),  # Log the productType before override
                            )
                        device["productType"] = "appliance"  # Force to 'appliance'.

                    # Log the final productType for MX devices after all modifications.
                    # This helps in debugging productType issues for MX devices.
                    if device.get("model", "").upper().startswith("MX"):
                        _LOGGER.debug(
                            "Final productType for MX device %s (Serial: %s) before leaving fetch_all_data: %s",
                            device.get("name", "Unknown"),
                            serial,
                            device.get("productType"),
                        )
                elif (
                    serial
                ):  # If device serial exists but no status entry was found for it.
                    _LOGGER.debug(
                        "No specific status entry found for device %s. It may retain a prior status or have none.",
                        serial,
                    )
        elif devices:  # If devices list exists but device_statuses_map is empty.
            _LOGGER.debug(
                "No device statuses were successfully mapped, skipping merge."
            )

        # Step 3: Fetch firmware upgrade data for the organization.
        # This data is used to determine if devices have pending upgrades or are up-to-date.
        firmware_upgrade_data = (
            {}
        )  # Initialize as an empty dict; will be a list if successful.
        try:
            # Fetch firmware upgrade status for the entire organization.
            firmware_upgrade_data = (
                await self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                    organizationId=self.org_id
                )
            )
            _LOGGER.debug("Successfully fetched firmware upgrade data for org %s.", self.org_id)
        except MerakiSDKAPIError as e:
            # Log API errors but continue, as firmware status is non-critical.
            _LOGGER.warning(
                "SDK API error fetching firmware upgrade data for org %s: "
                "Status %s, Reason: %s. Firmware data may be incomplete.",
                self.org_id,
                e.status,
                e.reason,
            )
            firmware_upgrade_data = (
                {}
            )  # Ensure it's an empty dict on error to prevent downstream issues.
        except Exception as e:
            # Log unexpected errors but continue.
            _LOGGER.exception(
                "Unexpected error fetching firmware upgrade data for org %s: %s. "
                "Firmware data may be incomplete.",
                self.org_id,
                e,
            )
            firmware_upgrade_data = {}  # Ensure it's an empty dict on error.

        # Step 4: Fetch additional details for MR (wireless) and MX (appliance) devices.
        # This is done concurrently using asyncio.gather for efficiency.
        additional_device_detail_tasks = []
        if devices:  # Only proceed if there are devices.
            for device in devices:  # Iterate through the list of devices.
                device_model_upper = device.get(
                    "model", ""
                ).upper()  # Get model, convert to uppercase for reliable matching.
                serial = device.get("serial")

                if (
                    not serial
                ):  # Skip if device serial is missing, as it's needed for API calls.
                    _LOGGER.debug(
                        "Device %s (MAC: %s) has no serial, skipping additional detail tasks.",
                        device.get("name", "N/A"),
                        device.get("mac", "N/A"),
                    )
                    continue

                if device_model_upper.startswith("MR"):
                    # For MR devices (wireless access points), fetch client count and radio settings.
                    additional_device_detail_tasks.append(
                        self._async_get_mr_device_details(
                            device, serial
                        )  # Schedule task.
                    )
                elif device_model_upper.startswith("MX"):
                    # For MX devices (security appliances), fetch uplink and LAN DNS settings.
                    # These provide details about WAN connectivity and local network DNS.
                    additional_device_detail_tasks.append(
                        self._async_get_mx_device_uplink_settings(
                            device, self.meraki_client
                        )  # Schedule task.
                    )
                    additional_device_detail_tasks.append(
                        self._async_get_mx_lan_dns_settings(
                            device, self.meraki_client
                        )  # Schedule task.
                    )

        if additional_device_detail_tasks:  # If there are tasks to run.
            await asyncio.gather(
                *additional_device_detail_tasks
            )  # Execute all scheduled tasks concurrently.

        # Step 5: Process firmware upgrade data and merge into device dictionaries.
        if devices:  # Check if there are devices to process.
            # Ensure firmware_upgrade_data is a list before iterating.
            # The API might return a single dict or other types on error/empty.
            if not isinstance(firmware_upgrade_data, list):
                _LOGGER.warning(
                    "firmware_upgrade_data is not a list (type: %s), "
                    "cannot process firmware status for devices. Value: %s",
                    type(firmware_upgrade_data).__name__,
                    str(firmware_upgrade_data)[
                        :200
                    ],  # Log a snippet of the data for debugging.
                )
                # If data is not as expected, mark all devices with default firmware status.
                for device in devices:
                    device["firmware_up_to_date"] = (
                        False  # Assume not up-to-date if data is bad.
                    )
                    device["latest_firmware_version"] = device.get(
                        "firmware", "N/A"
                    )  # Use current as latest known.
            elif (
                not firmware_upgrade_data
            ):  # If the list is empty (no pending or recent upgrades).
                _LOGGER.debug(
                    "firmware_upgrade_data is an empty list. "
                    "No specific upgrade information available for org %s.", self.org_id
                )
                # Assume all devices are up-to-date if no upgrade info is present.
                # This interpretation might need adjustment based on API behavior for fully up-to-date orgs.
                for device in devices:
                    device["firmware_up_to_date"] = (
                        True  # Or False, depending on desired default if API gives no info.
                    )
                    device["latest_firmware_version"] = device.get("firmware", "N/A")
            else:  # Process each device against the firmware upgrade data.
                _LOGGER.debug("Starting to process firmware data list for devices for org %s.", self.org_id)
                # if _LOGGER.isEnabledFor(logging.DEBUG): # Conditional logging for performance.
                #     _LOGGER.debug(
                #         "Sample firmware_upgrade_data item: %s",
                #         str(firmware_upgrade_data[0])[:300] # Log sample for debugging.
                #     )

                for device in devices:  # Iterate through each device.
                    device_serial = device.get("serial")
                    device_model = device.get("model", "")
                    current_device_firmware = device.get("firmware")
                    is_up_to_date_bool = (
                        False  # Default assumption: not up-to-date unless confirmed.
                    )
                    latest_known_version = (
                        current_device_firmware if current_device_firmware else "N/A"
                    )  # Default to current.
                    found_specific_info_for_device = (
                        False  # Flag to track if we found info for this device.
                    )

                    # Iterate through each entry in the firmware upgrade data from the organization.
                    for upgrade_item in firmware_upgrade_data:
                        if not isinstance(
                            upgrade_item, dict
                        ):  # Skip malformed entries.
                            _LOGGER.warning(
                                "Skipping non-dictionary item in firmware_upgrade_data list: %s",
                                str(upgrade_item)[:200],
                            )
                            continue

                        item_serial = upgrade_item.get("serial")
                        # Check if this upgrade entry is for the current device.
                        if item_serial and item_serial == device_serial:
                            _LOGGER.debug(
                                "Found firmware info by serial for %s",
                                device_serial,
                            )
                            # 'nextUpgrade' usually contains info about a scheduled upgrade.
                            next_upgrade_info = upgrade_item.get("nextUpgrade")
                            if isinstance(next_upgrade_info, dict):
                                # 'toVersion' indicates the version for the scheduled upgrade.
                                to_version_info = next_upgrade_info.get("toVersion")
                                if isinstance(to_version_info, dict):
                                    # This is the target version of the *next scheduled* upgrade.
                                    latest_known_version = to_version_info.get(
                                        "version", latest_known_version
                                    )
                                    # If there's a nextUpgrade, it implies the current one is not the latest.
                                    is_up_to_date_bool = False
                                else:
                                    # If no 'toVersion', check the general 'status' of the upgrade item.
                                    # This part handles cases where 'nextUpgrade' exists but 'toVersion' might be missing or structured differently.
                                    item_status = str(
                                        upgrade_item.get("status", "")
                                    ).lower()
                                    if item_status == "up-to-date":
                                        is_up_to_date_bool = True
                                        latest_known_version = (
                                            current_device_firmware
                                            if current_device_firmware
                                            else "N/A"
                                        )
                                    elif item_status == "has-newer-stable-version":
                                        # This status explicitly states a newer version is available.
                                        is_up_to_date_bool = False
                                        # 'availableVersions' might list newer versions, take the first as latest.
                                        available_versions = upgrade_item.get(
                                            "availableVersions"
                                        )
                                        if (
                                            isinstance(available_versions, list)
                                            and available_versions
                                        ):
                                            latest_known_version = available_versions[
                                                0
                                            ].get("version", latest_known_version)
                            else:
                                # If no 'nextUpgrade' info, rely on 'status' or 'latestVersion' field from the upgrade item.
                                item_status = str(
                                    upgrade_item.get("status", "")
                                ).lower()
                                if item_status == "up-to-date":
                                    is_up_to_date_bool = True
                                    # If status is up-to-date, current firmware is the latest known.
                                    latest_known_version = (
                                        current_device_firmware
                                        if current_device_firmware
                                        else "N/A"
                                    )
                                elif upgrade_item.get(
                                    "latestVersion"
                                ):  # Some API versions might provide this directly.
                                    latest_known_version = upgrade_item.get(
                                        "latestVersion"
                                    )
                                    # If latestVersion is present and different from current, it's not up-to-date.
                                    # This will be checked by the final comparison below.

                            # Final check: if current firmware matches the determined latest_known_version, it's up-to-date.
                            # This handles cases where 'status' might be misleading if 'latestVersion' or 'toVersion' is the same as current.
                            if (
                                current_device_firmware
                                and current_device_firmware == latest_known_version
                            ):
                                is_up_to_date_bool = True

                            found_specific_info_for_device = True
                            break  # Found info for this device, no need to check other upgrade_items.

                    # After checking all upgrade_items, if no specific info was found for this device:
                    if not found_specific_info_for_device and not firmware_upgrade_data:
                        # If firmware_upgrade_data was empty to begin with (no org-level upgrade info), assume up-to-date.
                        is_up_to_date_bool = True
                        latest_known_version = (
                            current_device_firmware
                            if current_device_firmware
                            else "N/A"
                        )
                    elif not found_specific_info_for_device:
                        # If upgrade data was available but no entry for this serial, make a best guess.
                        # This path implies we don't have definitive info for this device from the API.
                        # It's safer to assume not up-to-date or rely on comparison if current_device_firmware exists.
                        _LOGGER.debug(
                            "No specific firmware upgrade info found for device %s by serial.",
                            device_serial,
                        )
                        if (
                            current_device_firmware
                        ):  # If we have current firmware, compare with default latest_known_version (which was init with current).
                            is_up_to_date_bool = (
                                current_device_firmware == latest_known_version
                            )
                        # If no current_device_firmware, is_up_to_date_bool remains False (initial default).

                    # Store the determined firmware status in the device dictionary.
                    device["firmware_up_to_date"] = is_up_to_date_bool
                    device["latest_firmware_version"] = latest_known_version
                    _LOGGER.debug(
                        "Device %s (Model: %s, Current FW: %s): Up-to-date: %s, Latest Known: %s",
                        device_serial,
                        device_model,
                        current_device_firmware,
                        is_up_to_date_bool,
                        latest_known_version,
                    )
        else:  # No devices available to process.
            _LOGGER.debug(
                "No devices available to process firmware data for org %s.", self.org_id
            )

        # Step 6: Fetch SSIDs for each network.
        ssids: List[Dict[str, Any]] = []
        for (
            network
        ) in networks:  # Iterate through the list of networks obtained earlier.
            network_id: str = network["id"]  # Get network ID.
            try:
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
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
                        "Error fetching SSIDs for network %s was not handled by async_get_network_ssids: %s. Status: %s, Reason: %s. Skipping.",
                        network_id,
                        e,
                        e.status,
                        e.reason,
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
                        "SSID data result was None for network %s, SSIDs for this network will be skipped.",
                        network_id,
                    )
            except (
                Exception
            ) as e:  # Catch any other unexpected errors during processing of a network.
                _LOGGER.exception(
                    "Unexpected error processing network %s for SSID data: %s. Skipping this network's SSIDs.",
                    network_id,
                    e,
                )

        # Step 7: Fetch all clients across all networks.
        all_clients: List[Dict[str, Any]] = []
        if networks:  # Only proceed if networks list is available.
            for network in networks:  # Iterate through each network.
                network_id = network["id"]
                try:
                    _LOGGER.debug("Fetching clients for network ID: %s", network_id)
                    # Fetch clients for the current network. Timespan of 300 seconds (5 minutes)
                    # is used to get recently active clients. This helps in keeping the data fresh
                    # and manageable.
                    network_clients_data = (
                        await self.meraki_client.networks.getNetworkClients(
                            network_id,
                            timespan=300,  # Use a short timespan for recent clients.
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
                            "Fetched %d clients for network %s",
                            len(network_clients_data),
                            network_id,
                        )
                    else:  # No clients found for this network in the timespan.
                        _LOGGER.debug(
                            "No clients found for network %s in the given timespan.",
                            network_id,
                        )
                except (
                    MerakiSDKAPIError
                ) as e:  # Handle API errors during client fetching for a network.
                    _LOGGER.warning(
                        "Meraki SDK API error fetching clients for network %s: %s. Status: %s, Reason: %s. Skipping this network's clients.",
                        network_id,
                        e,
                        e.status,
                        e.reason,
                    )
                except Exception as e:  # Handle other unexpected errors.
                    _LOGGER.exception(
                        "Unexpected error fetching clients for network %s: %s. Skipping this network's clients.",
                        network_id,
                        e,
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

        _LOGGER.debug("Client counts for org %s: SSID: %d, Wireless: %d, Appliance: %d",
                      self.org_id, clients_on_ssids, clients_on_wireless, clients_on_appliances)

        # Step 9: Return all fetched and processed data.
        # This dictionary forms the basis for what coordinators and entities will use.
        return {
            "devices": devices,
            "networks": networks,
            "ssids": ssids,
            "clients": all_clients,
            "clients_on_ssids": clients_on_ssids,
            "clients_on_appliances": clients_on_appliances,
            "clients_on_wireless": clients_on_wireless,
        }

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

        try:
            _LOGGER.debug(f"Fetching client count for MR device {device.get('name', 'Unknown')} (Serial: {serial})")
            clients_data = await self.meraki_client.devices.getDeviceClients(
                serial=serial
            )
            _LOGGER.debug(f"Raw clients_data for MR device {serial}: {clients_data}")

            if clients_data is not None: # Will be a list, potentially empty
                device["connected_clients_count"] = len(clients_data)
                _LOGGER.debug(f"Set connected_clients_count to {device['connected_clients_count']} for MR device {serial} (from len).")
            else:
                # This case implies API returned None, not an empty list.
                # device["connected_clients_count"] is already 0 from initialization
                _LOGGER.debug(f"Clients_data was None for MR device {serial}. connected_clients_count remains 0.")

        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch client count for MR device %s (Serial: %s): API Error %s - %s. Setting client count to 0.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            device["connected_clients_count"] = 0 # Explicitly ensure it's 0
            _LOGGER.debug(f"Set connected_clients_count to 0 for MR device {serial} due to MerakiSDKAPIError.")

        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching client count for MR device %s (Serial: %s). Setting client count to 0.",
                device.get("name", "Unknown"),
                serial,
            )
            device["connected_clients_count"] = 0 # Explicitly ensure it's 0
            _LOGGER.debug(f"Set connected_clients_count to 0 for MR device {serial} due to general Exception.")

        _LOGGER.debug(f"Final connected_clients_count for MR device {serial} before radio settings: {device.get('connected_clients_count')}")

        try:
            _LOGGER.debug(f"Fetching radio settings for MR device {serial}")
            radio_settings_data = (
                await self.meraki_client.wireless.getDeviceWirelessRadioSettings(
                    serial=serial
                )
            )
            device["radio_settings"] = radio_settings_data
            _LOGGER.debug(f"Successfully fetched radio_settings for MR device {serial}")
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch radio settings for MR device %s (Serial: %s): API Error %s - %s. Setting radio_settings to None.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            device["radio_settings"] = None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching radio settings for MR device %s (Serial: %s). Setting radio_settings to None.",
                device.get("name", "Unknown"),
                serial,
            )
            device["radio_settings"] = None

        _LOGGER.debug(f"Finished _async_get_mr_device_details for {serial}. Client count: {device.get('connected_clients_count')}, Radio settings type: {type(device.get('radio_settings')).__name__}")

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            # Call SDK to get networks for the organization.
            _LOGGER.debug(
                "Executing async_get_networks with organizations.getOrganizationNetworks(organizationId=%s).",
                org_id,
            )
            org_networks = (
                await self.meraki_client.organizations.getOrganizationNetworks(
                    organizationId=org_id
                )
            )
            # Handle cases where API might return None or an empty list.
            if org_networks is None:  # If API response is literally None.
                _LOGGER.warning(
                    "Call to organizations.getOrganizationNetworks for org ID %s returned None.",
                    org_id,
                )
                return None  # Return None to indicate failure or no data.
            if not org_networks:  # If the list is empty.
                _LOGGER.warning(
                    "No networks found for organization ID %s using organizations.getOrganizationNetworks.",
                    org_id,
                )
                return None  # Or return [] if an empty list is a more desired "valid but no data" response.
            _LOGGER.debug(
                "Successfully fetched %d networks for org ID %s using organizations.getOrganizationNetworks.",
                len(org_networks),
                org_id,
            )
            return org_networks
        except MerakiSDKAPIError as e:
            # Log API errors and return None to indicate failure.
            _LOGGER.warning(
                "SDK API error during getNetworks or filtering for org %s: Status %s, Reason: %s. Returning None.",
                org_id,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:  # Catch any other unexpected error.
            # Log unexpected errors and return None.
            _LOGGER.exception(
                "Unexpected error during getNetworks or filtering for org %s: %s. Returning None.",
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
            # Call SDK to get all devices in the organization.
            devices_data = (
                await self.meraki_client.organizations.getOrganizationDevices(org_id)
            )
            if devices_data:  # Log count if data is received.
                _LOGGER.debug("Received %d devices from SDK for org %s.", len(devices_data), org_id)
            else:  # Log if no data or empty list.
                _LOGGER.debug("Received no devices_data from SDK (None or empty list) for org %s.", org_id)
            return devices_data
        except MerakiSDKAPIError as e:
            # Log API errors and return None.
            _LOGGER.warning(
                "SDK API error fetching devices for org %s: Status %s, Reason: %s. Returning None.",
                org_id,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:  # Catch any other unexpected error.
            # Log unexpected errors and return None.
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
            # Call SDK to get SSIDs for the given network.
            return await self.meraki_client.wireless.getNetworkWirelessSsids(
                networkId=network_id
            )
        except MerakiSDKAPIError as e:
            # Handle 404 specifically: network might not have wireless capabilities or SSIDs.
            # This is a common case for non-wireless networks (e.g., MX only networks).
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for network %s (likely no wireless capabilities or SSIDs configured). Returning empty list.",
                    network_id,
                )
                return (
                    []
                )  # Return empty list for 404, as it's a valid state (no SSIDs).
            # Log other API errors and return None to indicate failure for this network's SSIDs.
            _LOGGER.warning(
                "SDK API error fetching SSIDs for network %s: Status %s, Reason: %s. Returning None for this network's SSIDs.",
                network_id,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:  # Catch any other unexpected error.
            # Log unexpected errors and return None.
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for network %s: %s. Returning None.",
                network_id,
                e,
            )
            return None

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
                "Cannot fetch uplink settings for MX device %s: missing serial.",
                device.get("name", "Unknown"),
            )
            return

        _LOGGER.debug(
            "Fetching uplink settings for MX device %s (Serial: %s)",
            device.get("name", "Unknown"),
            serial,
        )

        # Initialize DNS server lists for the device to ensure they always exist, even if fetching fails or data is missing.
        # This prevents KeyError later if the lists are not populated.
        device["wan1_dns_servers"] = []
        device["wan2_dns_servers"] = []
        # Add other WANs here if needed, e.g., device["wan3_dns_servers"] = []

        try:
            # Fetch uplink settings for the specific MX device by its serial.
            uplink_settings = await client.appliance.getDeviceApplianceUplinksSettings(
                serial=serial
            )
            # _LOGGER.debug("Raw uplink settings for %s: %s", serial, uplink_settings) # Optional: log raw response for deep debugging.

            if uplink_settings:  # Check if any settings were returned.
                # Expected structure: uplink_settings = {"interfaces": {"wan1": {...}, "wan2": {...}}}
                interfaces = uplink_settings.get(
                    "interfaces", {}
                )  # Get the 'interfaces' dictionary, default to empty if not found.
                wan_interface_keys = [
                    "wan1",
                    "wan2",
                ]  # Define which WAN interfaces to check (e.g., "wan1", "wan2", "cellular").

                for (
                    interface_name
                ) in (
                    wan_interface_keys
                ):  # Iterate through defined WAN interfaces (wan1, wan2).
                    current_wan_dns_ips = (
                        []
                    )  # Temporary list to store DNS IPs for the current WAN interface.
                    interface_settings = interfaces.get(
                        interface_name, {}
                    )  # Get settings for the specific interface (e.g., wan1).

                    if interface_settings:  # If settings for this interface exist.
                        # Primary way to get DNS: via 'svis' -> 'ipv4' -> 'nameservers'
                        # This structure is often found in newer Meraki API versions or more detailed responses.
                        # Expected structure: interface_settings.svis.ipv4.nameservers = [{"addresses": ["ip1", "ip2"], "protocol": "ipv4"}]
                        svis_data = interface_settings.get("svis")
                        if isinstance(
                            svis_data, dict
                        ):  # Check if 'svis' data is a dictionary.
                            ipv4_data = svis_data.get("ipv4")
                            if isinstance(
                                ipv4_data, dict
                            ):  # Check if 'ipv4' data is a dictionary.
                                nameservers_list = ipv4_data.get("nameservers")
                                if isinstance(
                                    nameservers_list, list
                                ):  # Check if 'nameservers' is a list.
                                    for (
                                        ns_entry
                                    ) in (
                                        nameservers_list
                                    ):  # Each ns_entry is like {"addresses": ["ip1", "ip2"], "protocol": "ipv4"}
                                        if isinstance(ns_entry, dict) and isinstance(
                                            ns_entry.get("addresses"), list
                                        ):  # Validate structure.
                                            for ip_addr in ns_entry.get(
                                                "addresses", []
                                            ):  # Iterate through IPs in "addresses".
                                                if (
                                                    isinstance(ip_addr, str)
                                                    and ip_addr
                                                    not in current_wan_dns_ips
                                                ):  # Avoid duplicates.
                                                    current_wan_dns_ips.append(ip_addr)

                        # Fallback: Check 'dnsServers' directly under interface_settings
                        # This is a more common or older way the API might provide DNS servers.
                        # Expected structure: interface_settings.dnsServers = ["ip1", "ip2"] or "ip1,ip2" (string)
                        if (
                            not current_wan_dns_ips
                        ):  # Only if primary method didn't yield results.
                            dns_servers_field = interface_settings.get("dnsServers")
                            if isinstance(
                                dns_servers_field, list
                            ):  # If it's a list of IPs.
                                for dns_entry in dns_servers_field:
                                    if isinstance(dns_entry, str):
                                        # Basic validation for an IP address string (contains '.' for IPv4 or ':' for IPv6).
                                        if (
                                            "." in dns_entry or ":" in dns_entry
                                        ):  # Simple check if it looks like an IP.
                                            if (
                                                dns_entry not in current_wan_dns_ips
                                            ):  # Avoid duplicates.
                                                current_wan_dns_ips.append(dns_entry)
                            elif isinstance(
                                dns_servers_field, str
                            ):  # Sometimes it might be a comma-separated string or single IP.
                                # Basic validation for an IP address string.
                                if (
                                    "." in dns_servers_field or ":" in dns_servers_field
                                ):  # Simple check.
                                    if (
                                        dns_servers_field not in current_wan_dns_ips
                                    ):  # Assuming it's a single IP if string.
                                        current_wan_dns_ips.append(dns_servers_field)

                    # Second Fallback: Check device-level fields like 'wan1PrimaryDns', 'wan1SecondaryDns'
                    # These might be present in the main device data (from /status endpoint) if not in uplink_settings specifically.
                    # This is a less common source but provides robustness if other paths fail.
                    if (
                        not current_wan_dns_ips
                    ):  # Only if previous methods yielded no results.
                        primary_dns_key = (
                            f"{interface_name}PrimaryDns"  # e.g., "wan1PrimaryDns"
                        )
                        secondary_dns_key = (
                            f"{interface_name}SecondaryDns"  # e.g., "wan1SecondaryDns"
                        )
                        primary_dns = device.get(
                            primary_dns_key
                        )  # Get from the main device dictionary (already fetched status).
                        if (
                            primary_dns
                            and isinstance(primary_dns, str)
                            and primary_dns not in current_wan_dns_ips
                        ):
                            current_wan_dns_ips.append(primary_dns)
                        secondary_dns = device.get(secondary_dns_key)
                        if (
                            secondary_dns
                            and isinstance(secondary_dns, str)
                            and secondary_dns not in current_wan_dns_ips
                        ):
                            current_wan_dns_ips.append(secondary_dns)

                    # Store the collected DNS IPs for this WAN interface in the main device dictionary.
                    # This makes it available for sensors or other logic.
                    device[f"{interface_name}_dns_servers"] = current_wan_dns_ips
                    _LOGGER.debug(
                        "Populated %s_dns_servers for %s: %s",
                        interface_name,
                        serial,
                        device[f"{interface_name}_dns_servers"],
                    )
            else:  # If no uplink_settings data was returned at all for the device.
                _LOGGER.debug(
                    "No uplink settings data returned for MX device %s (Serial: %s). "
                    "DNS server lists will remain default (empty or from device status).",
                    device.get("name", "Unknown"),
                    serial,
                )
        except MerakiSDKAPIError as e:
            # Log API errors and ensure DNS lists remain empty (as initialized).
            _LOGGER.warning(
                "Failed to fetch uplink settings for MX device %s (Serial: %s): "
                "API Error %s - %s. DNS server info will be unavailable.",
                device.get("name", "Unknown"),
                serial,
                e.status,
                e.reason,
            )
            # Defaults are already set at the beginning of the try block, so no specific action needed here.
        except Exception as e:  # Catch any other unexpected error.
            # Log unexpected errors.
            _LOGGER.exception(
                "Unexpected error fetching uplink settings for MX device %s (Serial: %s): %s. "
                "DNS server info will be unavailable.",
                device.get("name", "Unknown"),
                serial,
                e,
            )
            # Defaults are already set.

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
                "Cannot fetch LAN DNS settings for MX device %s (Serial: %s): missing networkId.",
                device_name,
                serial,
            )
            device["lan_dns_settings"] = (
                {}
            )  # Ensure the key exists in the device dict, even if empty.
            return

        _LOGGER.debug(
            "Fetching LAN DNS (VLAN settings) for MX device %s (Serial: %s, Network: %s)",
            device_name,
            serial,
            network_id,
        )

        lan_dns_by_vlan: Dict[str, Any] = (
            {}
        )  # Dictionary to store DNS settings per VLAN.
        vlan_list_to_iterate: List[Dict[str, Any]] = (
            []
        )  # List to hold VLAN data from API for consistent processing.
        try:
            # Fetch VLAN settings for the network associated with the MX device.
            # The API might return a list of VLANs or a single dictionary if only one VLAN is configured.
            vlan_settings_response = (
                await client.appliance.getNetworkApplianceVlansSettings(
                    networkId=network_id
                )
            )

            # Standardize response to be a list for consistent processing logic.
            if isinstance(
                vlan_settings_response, dict
            ):  # If API returns a single VLAN object.
                _LOGGER.debug(
                    "Received single dictionary for VLAN settings for network %s (Serial: %s). Wrapping in a list.",
                    network_id,
                    serial,
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
                    "No VLANs configured or endpoint not applicable for network %s (Serial: %s) (response is None).",
                    network_id,
                    serial,
                )
                # vlan_list_to_iterate remains empty, which is handled gracefully below.
            else:  # Unexpected response type from the API.
                _LOGGER.warning(
                    "Unexpected response type for VLAN settings for network %s (Serial: %s): %s. Expected list or dict.",
                    network_id,
                    serial,
                    type(vlan_settings_response).__name__,
                )
                # vlan_list_to_iterate remains empty.

            if vlan_list_to_iterate:  # If there are VLANs to process.
                _LOGGER.debug(
                    "Processing %d VLAN entries for network %s.",
                    len(vlan_list_to_iterate),
                    network_id,
                )
                for (
                    vlan_data
                ) in vlan_list_to_iterate:  # Iterate through each VLAN's data.
                    if not isinstance(vlan_data, dict):  # Skip malformed entries.
                        _LOGGER.warning(
                            "Skipping non-dictionary item in VLAN settings list for network %s: %s",
                            network_id,
                            vlan_data,
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
                                "VLAN %s on %s using custom DNS: %s",
                                vlan_key,
                                serial,
                                custom_dns_servers,
                            )
                        else:  # If set to "custom_servers" but no IPs are listed.
                            lan_dns_by_vlan[vlan_key] = []  # Store as empty list.
                            _LOGGER.debug(
                                "VLAN %s on %s set to 'custom_servers' but no IPs provided.",
                                vlan_key,
                                serial,
                            )
                    elif (
                        dns_nameservers_setting
                    ):  # If not "custom_servers", store the setting string itself (e.g., "google_dns").
                        lan_dns_by_vlan[vlan_key] = dns_nameservers_setting
                        _LOGGER.debug(
                            "VLAN %s on %s using preset DNS: %s",
                            vlan_key,
                            serial,
                            dns_nameservers_setting,
                        )
                    else:  # If no specific DNS setting ('dnsNameservers') found for the VLAN.
                        lan_dns_by_vlan[vlan_key] = (
                            "Not configured"  # Indicate not configured.
                        )
                        _LOGGER.debug(
                            "VLAN %s on %s has no explicit DNS configuration.",
                            vlan_key,
                            serial,
                        )
            # If vlan_list_to_iterate is empty (e.g., from None response or unexpected type), this loop is skipped.

        except MerakiSDKAPIError as e:
            # Handle 404 specifically: network might not have VLANs or endpoint not applicable (e.g., non-MX device).
            if e.status == 404:
                _LOGGER.debug(
                    "No VLAN settings found for network %s (Serial: %s) (404 Error). "
                    "This may be normal if no VLANs are configured or device is not an appliance.",
                    network_id,
                    serial,
                )
            else:  # Log other API errors.
                _LOGGER.warning(
                    "Failed to fetch LAN DNS settings for MX device %s (Serial: %s, Network: %s): "
                    "API Error %s - %s. LAN DNS settings will be unavailable.",
                    device_name,
                    serial,
                    network_id,
                    e.status,
                    e.reason,
                )
        except Exception as e:  # Catch any other unexpected error.
            # Log unexpected errors.
            _LOGGER.exception(
                "Unexpected error fetching LAN DNS settings for MX device %s (Serial: %s, Network: %s): %s. "
                "LAN DNS settings will be unavailable.",
                device_name,
                serial,
                network_id,
                e,
            )
        # Store the collected LAN DNS settings in the main device dictionary.
        # This makes it available for sensors or other logic.
        device["lan_dns_settings"] = lan_dns_by_vlan
        _LOGGER.debug(
            "Final LAN DNS settings for %s (Serial: %s): %s",
            device_name,
            serial,
            lan_dns_by_vlan,
        )
