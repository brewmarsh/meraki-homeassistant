"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices (including tags), SSIDs, and device-specific details
like client counts and radio settings for MR devices, using the Meraki SDK.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Awaitable  # Added Awaitable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from ..api.meraki_api import MerakiAPIClient
from .meraki_device_types import (
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
            meraki_client: An instance of the SDK-based `MerakiAPIClient` used for API communication.
        """
        self.meraki_client: MerakiAPIClient = meraki_client
        self.org_id: str = meraki_client.org_id  # Organization ID from the client
        self._api_call_semaphore = asyncio.Semaphore(5) # Allow up to 5 concurrent API calls
        self.devices: list[dict[str, Any]] | None = None
        # Fetched on demand, can be empty
        self.networks: list[dict[str, Any]] | None = None

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # hass is retained for potential future use or context.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        Orchestrates calls to retrieve networks, devices (with their tags & status),
        SSIDs, clients, and firmware upgrade details. For specific device types (MR, MX, MV),
        it fetches additional relevant details.

        Args:
            hass: The Home Assistant instance. Currently unused but retained for potential
                  future use or consistency with Home Assistant patterns.

        Returns:
            A dictionary containing lists of processed data for 'devices', 'networks',
            'ssids', 'clients', and details like 'clients_on_ssids',
            'clients_on_appliances', 'clients_on_wireless', and 'org_name'.
            The 'devices' list includes merged status, tags, and device-specific details.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched after retries/error handling within helper methods,
                          preventing a meaningful update.
            MerakiSDKAPIError: For underlying API communication issues from the SDK
                               that are not handled by individual fetch methods and
                               escalate to this level.
        """
        _LOGGER.debug(f"Fetching all data for organization ID: {self.org_id} using SDK")

        # Step 1: Concurrently fetch foundational data
        # Networks, Devices, Device Statuses, Firmware Upgrades
        results = await asyncio.gather(
            self.meraki_client.organizations.getOrganizations(),
            self.async_get_networks(self.org_id),
            self.async_get_organization_devices(self.org_id),
            self.meraki_client.organizations.getOrganizationDevicesStatuses(
                organizationId=self.org_id, total_pages="all"
            ),
            self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                organizationId=self.org_id
            ),
            return_exceptions=True,
        )

        organizations = results[0]
        org_details = None
        if isinstance(organizations, list):
            for org in organizations:
                if org.get("id") == self.org_id:
                    org_details = org
                    break

        # Unpack results and handle errors
        networks: Optional[List[Dict[str, Any]]] = None
        devices: Optional[List[Dict[str, Any]]] = None
        statuses_data: Optional[List[Dict[str, Any]]] = None
        firmware_upgrade_data_raw: Optional[List[Dict[str, Any]]] = None  # Raw from API

        if isinstance(results[0], Exception):
            _LOGGER.error(
                f"Critical error fetching networks for org {self.org_id}: {results[0]}"
            )
        else:
            networks = results[0]

        if isinstance(results[1], Exception):
            _LOGGER.error(
                f"Critical error fetching devices for org {self.org_id}: {results[1]}"
            )
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
            firmware_upgrade_data_raw = None
        elif isinstance(results[3], Exception):
            _LOGGER.exception(
                f"Unexpected error fetching firmware upgrade data for org {self.org_id}: {results[3]}. "
                "Firmware data may be incomplete."
            )
            firmware_upgrade_data_raw = None
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
        if (
            devices is None
        ):  # This check is after results unpacking, devices could be None due to fetch error
            _LOGGER.error(
                f"Meraki devices data is None for org ID: {self.org_id} after fetch. Aborting update."
            )
            raise UpdateFailed(
                f"Fetched Meraki devices data is None for org {self.org_id}."
            )
        if not isinstance(devices, list):
            _LOGGER.error(
                f"Fetched Meraki devices data is not a list (type: {type(devices).__name__}) for org ID: {self.org_id}. Aborting update."
            )
            raise UpdateFailed(f"Invalid devices data format for org {self.org_id}.")
        if not isinstance(
            networks, list
        ):  # Networks is checked for None earlier, this is for type
            _LOGGER.error(
                f"Fetched Meraki networks data is not a list (type: {type(networks).__name__}) for org ID: {self.org_id}. Aborting update."
            )
            raise UpdateFailed(f"Invalid networks data format for org {self.org_id}.")

        # Step 2.1: Process Device Statuses (already fetched)
        device_statuses_map = {}
        if statuses_data and not isinstance(statuses_data, list):
            _LOGGER.warning(
                f"Device status data was fetched but is not a list (type: {type(statuses_data).__name__}). Cannot process statuses."
            )
            statuses_data = None  # Treat as if no statuses were fetched

        if statuses_data:
            for status_entry in statuses_data:
                if not isinstance(status_entry, dict):
                    _LOGGER.warning(
                        "Skipping non-dictionary status_entry: %s",
                        str(status_entry)[:100],
                    )
                    continue
                if status_entry.get("serial"):
                    device_statuses_map[status_entry["serial"]] = status_entry
        elif devices:
            _LOGGER.warning(
                f"Device status data was not successfully fetched or was empty for org {self.org_id}. Status-dependent info may be missing."
            )

        # Step 2.2: Merge Statuses into Devices
        if device_statuses_map:  # Only proceed if there's something to merge
            for device_idx, device in enumerate(devices):
                if not isinstance(device, dict):
                    _LOGGER.warning(
                        "Skipping non-dictionary device item at index %d: %s",
                        device_idx,
                        str(device)[:100],
                    )
                    continue

                serial = device.get("serial")
                if serial and serial in device_statuses_map:
                    status_update_data = device_statuses_map[serial]
                    if not isinstance(
                        status_update_data, dict
                    ):  # Should be a dict if from device_statuses_map
                        _LOGGER.warning(
                            "Skipping non-dictionary status_update_data for serial %s: %s",
                            serial,
                            str(status_update_data)[:100],
                        )
                        continue

                    original_model = device.get("model", "")
                    original_product_type = device.get("productType")
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
        # devices is now confirmed to be a list
        for device_idx, device in enumerate(devices):
            if not isinstance(device, dict):
                _LOGGER.warning(
                    "Skipping non-dictionary device item at index %d for additional details: %s",
                    device_idx,
                    str(device)[:100],
                )
                continue

            device_model = device.get("model", "")
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
            # _LOGGER.debug(
            #     f"Device {serial} (Model: {device_model}) mapped to generic type: {generic_device_type}"
            # )

            # Call _async_get_mr_device_details if it's a "Wireless" device
            if generic_device_type == "Wireless":
                # _LOGGER.debug(
                #     f"Device {serial} is Wireless, scheduling _async_get_mr_device_details."
                # )
                additional_device_detail_tasks.append(
                    self._async_get_mr_device_details(device, serial)
                )
            elif device_model.upper().startswith("MX"):  # Keep existing MX logic as is
                # _LOGGER.debug(f"Device {serial} is MX, scheduling MX detail tasks.")
                additional_device_detail_tasks.append(
                    self._async_get_mx_device_uplink_settings(device)
                )
                additional_device_detail_tasks.append(
                    self._async_get_mx_lan_dns_settings(device)
                )
            # Check for Camera devices (MV)
            # Use productType (more reliable) or model prefix (fallback)
            elif device.get(
                "productType", ""
            ).lower() == "camera" or device_model.upper().startswith("MV"):
                # _LOGGER.debug(
                #     f"Device {serial} is Camera, scheduling _async_get_camera_video_settings."
                # )
                # Initialize externalRtspEnabled and rtspUrl to None before task creation
                device["externalRtspEnabled"] = None
                device["rtspUrl"] = None  # Initialize rtspUrl as well
                additional_device_detail_tasks.append(
                    self._async_get_camera_video_settings(device)
                )

        if additional_device_detail_tasks:  # If there are tasks to run.
            await asyncio.gather(
                *additional_device_detail_tasks
            )  # Execute all scheduled tasks concurrently.

        # Step 5: Process firmware upgrade data (now `firmware_upgrade_data_raw`) and merge into device dictionaries.
        firmware_info_map = {}
        if devices:  # Check if there are devices to process.
            if not isinstance(
                firmware_upgrade_data_raw, list
            ):  # Use the raw data variable
                _LOGGER.warning(
                    f"firmware_upgrade_data_raw is not a list (type: {type(firmware_upgrade_data_raw).__name__}), "  # Use the raw data variable
                    f"cannot process firmware status for devices. Value: {str(firmware_upgrade_data_raw)[:200]}"  # Use the raw data variable
                )
                # If data is not as expected, all devices will use default firmware status later.
            elif not firmware_upgrade_data_raw:  # Use the raw data variable
                _LOGGER.debug(
                    f"firmware_upgrade_data_raw is an empty list. "  # Use the raw data variable
                    f"No specific upgrade information available for org {self.org_id}."
                )
                # If list is empty, all devices will assume up-to-date status later.
            else:
                # _LOGGER.debug(
                #     f"Processing firmware upgrade data (raw) to build a map for org {self.org_id}."
                # ) # Removed
                for (
                    upgrade_item
                ) in firmware_upgrade_data_raw:  # Use the raw data variable
                    if not isinstance(upgrade_item, dict):
                        _LOGGER.warning(
                            f"Skipping non-dictionary item in firmware_upgrade_data_raw list: {str(upgrade_item)[:200]}"  # Use the raw data variable
                        )
                        continue

                    item_serial = upgrade_item.get("serial")
                    if not item_serial:
                        # _LOGGER.debug("Skipping firmware item with no serial.")
                        continue

                    is_item_up_to_date = False
                    latest_item_version = "N/A"

                    next_upgrade_info = upgrade_item.get("nextUpgrade")
                    if isinstance(next_upgrade_info, dict):
                        to_version_info = next_upgrade_info.get("toVersion")
                        if isinstance(to_version_info, dict):
                            latest_item_version_val = to_version_info.get("version", "N/A")
                            if latest_item_version_val:
                                latest_item_version = latest_item_version_val
                            else:
                                pass
                            is_item_up_to_date = False
                        else:
                            if (
                                to_version_info is not None
                            ):
                                _LOGGER.warning(
                                    "Firmware upgrade item for serial %s has 'toVersion' but it's not a dictionary: %s. Cannot determine scheduled version.",
                                    item_serial,
                                    str(to_version_info)[:100],
                                )
                            item_status = str(upgrade_item.get("status", "")).lower()
                            if item_status == "up-to-date":
                                is_item_up_to_date = True
                            elif item_status == "has-newer-stable-version":
                                is_item_up_to_date = False
                                available_versions = upgrade_item.get(
                                    "availableVersions"
                                )
                                if (
                                    isinstance(available_versions, list)
                                    and available_versions
                                ):
                                    if isinstance(available_versions[0], dict):
                                        latest_item_version_val = available_versions[0].get(
                                            "version", "N/A"
                                        )
                                        if latest_item_version_val:
                                            latest_item_version = latest_item_version_val
                                    else:
                                        _LOGGER.warning(
                                            "First item in 'availableVersions' for serial %s is not a dict: %s. Cannot determine latest available version.",
                                            item_serial,
                                            str(available_versions[0])[:100],
                                        )
                                elif (
                                    available_versions is not None
                                ):
                                    _LOGGER.warning(
                                        "'availableVersions' for serial %s is not a non-empty list: %s. Cannot determine latest available version.",
                                        item_serial,
                                        str(available_versions)[:100],
                                    )
                    elif (
                        next_upgrade_info is not None
                    ):
                        _LOGGER.warning(
                            "Firmware upgrade item for serial %s has 'nextUpgrade' but it's not a dictionary: %s.",
                            item_serial,
                            str(next_upgrade_info)[:100],
                        )
                        item_status = str(upgrade_item.get("status", "")).lower()
                        if item_status == "up-to-date":
                            is_item_up_to_date = True
                        elif (
                            item_status == "has-newer-stable-version"
                        ):
                            is_item_up_to_date = False
                            available_versions = upgrade_item.get(
                                "availableVersions"
                            )
                            if (
                                isinstance(available_versions, list)
                                and available_versions
                            ):
                                if isinstance(available_versions[0], dict):
                                    latest_item_version = available_versions[0].get(
                                        "version", "N/A"
                                    )
                                else:
                                    _LOGGER.warning(
                                        "First item in 'availableVersions' (no nextUpgrade path) for serial %s is not a dict: %s.",
                                        item_serial,
                                        str(available_versions[0])[:100],
                                    )
                            elif available_versions is not None:
                                _LOGGER.warning(
                                    "'availableVersions' (no nextUpgrade path) for serial %s is not a non-empty list: %s.",
                                    item_serial,
                                    str(available_versions)[:100],
                                )
                    else:
                        item_status = str(upgrade_item.get("status", "")).lower()
                        if item_status == "up-to-date":
                            is_item_up_to_date = True
                        elif upgrade_item.get("latestVersion"):
                            latest_item_version_val = upgrade_item.get("latestVersion")
                            if latest_item_version_val:
                                latest_item_version = latest_item_version_val
                        elif (
                            item_status == "has-newer-stable-version"
                        ):
                            is_item_up_to_date = False
                            available_versions = upgrade_item.get("availableVersions")
                            if (
                                isinstance(available_versions, list)
                                and available_versions
                            ):
                                latest_item_version = available_versions[0].get(
                                    "version", "N/A"
                                )

                    firmware_info_map[item_serial] = {
                        "api_reported_up_to_date": is_item_up_to_date,
                        "api_latest_version": latest_item_version,
                        "api_status": upgrade_item.get("status", "").lower(),
                    }

            for device in devices:
                device_serial = device.get("serial")
                current_device_firmware = device.get("firmware")

                is_up_to_date_bool = False
                latest_known_version = current_device_firmware if current_device_firmware else "N/A"

                if not isinstance(firmware_upgrade_data_raw, list):
                    is_up_to_date_bool = False
                elif not firmware_upgrade_data_raw:
                    is_up_to_date_bool = True
                elif device_serial and device_serial in firmware_info_map:
                    info = firmware_info_map[device_serial]
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
                            is_up_to_date_bool = False
                    elif api_reported_up_to_date:
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    else:
                        is_up_to_date_bool = False
                        if api_latest_version and api_latest_version != "N/A":
                            latest_known_version = api_latest_version

                    if current_device_firmware and current_device_firmware == latest_known_version:
                        is_up_to_date_bool = True
                else:
                    # _LOGGER.debug( # This log was already removed, but the block is being modified
                    #     f"No specific firmware upgrade info found for device {device_serial} in map. Using defaults."
                    # )
                    if current_device_firmware:
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware
                    else:
                        is_up_to_date_bool = False
                        latest_known_version = "N/A"

                device["firmware_up_to_date"] = is_up_to_date_bool
                device["latest_firmware_version"] = latest_known_version
        else:
            _LOGGER.debug(
                f"No devices available to process firmware data for org {self.org_id}."
            )

        # Step 6: Fetch SSIDs for each network.
        ssids: List[Dict[str, Any]] = []
        # networks is now confirmed to be a list
        for network_idx, network in enumerate(networks):
            if not isinstance(network, dict):
                _LOGGER.warning(
                    "Skipping non-dictionary network item at index %d for SSID fetching: %s",
                    network_idx,
                    str(network)[:100],
                )
                continue

            network_id = network.get("id")
            if (
                not network_id
            ):  # Should have been validated by caller if networks is from process_networks
                _LOGGER.warning(
                    "Network item at index %d missing 'id'. Skipping SSID fetch for this network: %s",
                    network_idx,
                    str(network)[:100],
                )
                continue

            try:
                # _LOGGER.debug(f"Fetching SSIDs for network ID: {network_id}")
                ssid_data_for_network = None
                try:
                    ssid_data_for_network = await self.async_get_network_ssids(network_id)
                except MerakiSDKAPIError as e:
                    _LOGGER.warning(
                        f"Error fetching SSIDs for network {network_id} was not handled by async_get_network_ssids: {e}. Status: {e.status}, Reason: {e.reason}. Skipping."
                    )
                if ssid_data_for_network:
                    for ssid_obj in ssid_data_for_network:
                        if isinstance(ssid_obj, dict):
                            if ssid_obj.get("networkId") is None:
                                ssid_obj["networkId"] = network_id
                                # _LOGGER.debug(
                                #     f"Added/updated networkId '{network_id}' for SSID '{ssid_obj.get('name')}' (Number: {ssid_obj.get('number')})"
                                # )
                        else:
                            _LOGGER.warning(
                                f"Found non-dict item in ssid_data_for_network: {ssid_obj}"
                            )
                    ssids.extend(ssid_data_for_network)
                elif ssid_data_for_network is None:
                    _LOGGER.info(
                        f"SSID data result was None for network {network_id}, SSIDs for this network will be skipped."
                    )
            except Exception as e:
                _LOGGER.exception(
                    f"Unexpected error processing network {network_id} for SSID data: {e}. Skipping this network's SSIDs."
                )

        # Step 7: Fetch all clients across all networks.
        all_clients: List[Dict[str, Any]] = []
        # networks is confirmed to be a list
        for network_idx, network in enumerate(networks):
            if not isinstance(
                network, dict
            ):  # Should have been caught if networks is from process_networks
                _LOGGER.warning(
                    "Skipping non-dictionary network item at index %d for client fetching: %s",
                    network_idx,
                    str(network)[:100],
                )
                continue

            network_id = network.get("id")  # Already validated if from process_networks
            if not network_id:
                _LOGGER.warning(
                    "Network item at index %d missing 'id'. Skipping client fetch for this network: %s",
                    network_idx,
                    str(network)[:100],
                )
                continue

            try:
                # _LOGGER.debug(f"Fetching clients for network ID: {network_id}")
                async with self._api_call_semaphore:
                    network_clients_data = (
                        await self.meraki_client.networks.getNetworkClients(
                            network_id,
                            timespan=3600,
                        )
                    )
                if not isinstance(network_clients_data, list):
                    _LOGGER.warning(
                        "Network clients data for network %s is not a list (type: %s). Skipping client processing for this network.",
                        network_id,
                        type(network_clients_data).__name__,
                    )
                    continue

                if network_clients_data:
                    for client_idx, client_data in enumerate(network_clients_data):
                        if not isinstance(client_data, dict):
                            _LOGGER.warning(
                                "Skipping non-dictionary client_data item at index %d for network %s: %s",
                                client_idx,
                                network_id,
                                str(client_data)[:100],
                            )
                            continue

                        mac_address = client_data.get("mac")
                        if not mac_address or not isinstance(mac_address, str):
                            _LOGGER.warning(
                                "Client data item at index %d for network %s missing or invalid 'mac' (type: %s, value: %s). Skipping this client.",
                                client_idx,
                                network_id,
                                type(mac_address).__name__,
                                str(mac_address)[:100],
                            )
                            continue

                        ap_serial = (
                            client_data.get("recentDeviceSerial")
                            or client_data.get("recentDeviceMac")
                            or client_data.get("deviceSerial")
                        )
                        client_entry = {
                            "mac": mac_address,
                            "ip": client_data.get("ip"),
                            "description": client_data.get("description"),
                            "status": client_data.get("status", "Online"),
                            "networkId": network_id,
                            "ap_serial": ap_serial,
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
                        all_clients.append(client_entry)
                    # _LOGGER.debug(
                    #     f"Fetched {len(network_clients_data)} clients for network {network_id}"
                    # ) # Reduced verbosity
                else:
                    _LOGGER.debug(
                        f"No clients found for network {network_id} in the given timespan."
                    )
            except (
                MerakiSDKAPIError
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.warning(
                    f"Meraki API call to get clients for network {network_id} returned a 404, which is handled as an empty list."
                )
            else:
                _LOGGER.error(
                    f"Meraki SDK API error fetching clients for network {network_id}: {e}. Status: {e.status}, Reason: {e.reason}. Skipping this network's clients."
                )
        except Exception as e:
            _LOGGER.exception(
                f"Unexpected error fetching clients for network {network_id}: {e}. Skipping this network's clients."
            )
        else:  # No networks available to fetch clients from.
            _LOGGER.info("No networks were found or available for this organization. Client data will be empty.")

        # Step 8: Aggregate client counts
        clients_on_ssids = 0
        clients_on_appliances = 0
        clients_on_wireless = 0

        device_serial_to_type_map = {}
        # devices is confirmed to be a list
        for device_idx, device in enumerate(devices):
            if not isinstance(device, dict):  # Should have been caught, but for safety
                _LOGGER.warning(
                    "Skipping non-dictionary device item at index %d for serial_to_type_map: %s",
                    device_idx,
                    str(device)[:100],
                )
                continue
            serial = device.get("serial")
            model = device.get("model", "")
            if not isinstance(
                model, str
            ):  # Ensure model is a string for map_meraki_model_to_device_type
                _LOGGER.warning(
                    "Device serial %s has non-string model (type: %s, value: %s). Using empty string for type mapping.",
                    serial,
                    type(model).__name__,
                    model,
                )
                model = ""
            if (
                serial
            ):  # model can be empty string, map_meraki_model_to_device_type should handle
                device_serial_to_type_map[serial] = map_meraki_model_to_device_type(
                    model
                )

        for client_idx, client in enumerate(all_clients):
            if not isinstance(
                client, dict
            ):  # all_clients should be list of dicts by now
                _LOGGER.warning(
                    "Skipping non-dictionary client item at index %d for counting: %s",
                    client_idx,
                    str(client)[:100],
                )
                continue

            if client.get("ssid"):
                clients_on_ssids += 1

            ap_serial = client.get("ap_serial")
            if ap_serial:  # ap_serial can be None
                device_type = device_serial_to_type_map.get(ap_serial)
                if device_type == "Wireless":
                    clients_on_wireless += 1
                elif device_type == "Appliance":
                    clients_on_appliances += 1
                    # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section
            # else: # No specific log needed if no ap_serial, normal case for some clients
            # Removed MERAKI_CLIENT_COUNT_DEBUG logs from this section

        # _LOGGER.debug(
        #     f"ApiFetcher: Calculated Organization-Wide Client Counts: SSID={clients_on_ssids}, Wireless={clients_on_wireless}, Appliance={clients_on_appliances}"
        # )
        # _LOGGER.debug(
        #     f"Client counts for org {self.org_id}: SSID: {clients_on_ssids}, Wireless: {clients_on_wireless}, Appliance: {clients_on_appliances}"
        # )

        # Step 9: Fetch organization details to get the organization name.
        org_details: Optional[Dict[str, Any]] = None
        org_name: Optional[str] = None
        try:
            # _LOGGER.debug(f"Fetching organization details for org ID: {self.org_id}")
            org_details = await self.meraki_client.organizations.getOrganization(
                organizationId=self.org_id
            )
            if org_details and isinstance(org_details, dict):
                org_name = org_details.get("name")
                # _LOGGER.debug(
                #     f"Successfully fetched organization name: {org_name} for org ID: {self.org_id}"
                # )
            else:
                _LOGGER.warning(
                    f"Could not extract organization name. Org details: {org_details}"
                )
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
        self,
        api_coro: Awaitable[Any],
        call_description: str,
        return_empty_list_on_404: bool = False,
    ) -> Optional[Any]:
        """Helper to make a Meraki API call and handle common exceptions.

        Args:
            api_coro: The coroutine representing the API call to execute.
            call_description: A human-readable description of the API call for logging.
            return_empty_list_on_404: If True, return an empty list on HTTP 404,
                                      otherwise returns None for 404.

        Returns:
            The result of the API call if successful, or None/empty list on error/404.
        """
        # _LOGGER.debug(f"Executing API call: {call_description}") # Reduced verbosity
        try:
            result = await api_coro
            # _LOGGER.debug(f"Successfully executed API call: {call_description}") # Reduced verbosity
            return result
        except UnboundLocalError as e:
            _LOGGER.error(f"UnboundLocalError during {call_description}: {e}. This is a bug in the meraki library.")
            return None
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.warning(
                    f"Meraki API call to {call_description} returned a 404, which is handled as an empty list."
                )
                return []
            _LOGGER.error(
                f"Meraki SDK API error during {call_description} for org {self.org_id}: Status {e.status}, Reason: {e.reason}."
            )
            return None
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

        async with self._api_call_semaphore:
            clients_data = await self._async_meraki_api_call(
                self.meraki_client.devices.getDeviceClients(serial=serial),
                f"getDeviceClients(serial={serial})",
            )

        if clients_data is not None:
            device["connected_clients_count"] = len(clients_data)
            # _LOGGER.debug(
            #     f"Set connected_clients_count to {len(clients_data)} for MR device {serial} (from len)."
            # )
        else:
            device["connected_clients_count"] = 0
            # _LOGGER.debug(
            #     f"Clients_data was None (call failed) for MR device {serial}. connected_clients_count remains 0."
            # )

        async with self._api_call_semaphore:
            radio_settings_data = await self._async_meraki_api_call(
                self.meraki_client.wireless.getDeviceWirelessRadioSettings(serial=serial),
                f"getDeviceWirelessRadioSettings(serial={serial})",
            )

        if radio_settings_data is not None:
            device["radio_settings"] = radio_settings_data
            # _LOGGER.debug(f"Successfully fetched radio_settings for MR device {serial}")
        else:
            device["radio_settings"] = None
            # _LOGGER.debug(
            #     f"Radio_settings_data was None (call failed) for MR device {serial}. radio_settings remains None."
            # )

        # _LOGGER.debug(
        #     f"Finished _async_get_mr_device_details for {serial}. Client count: {device.get('connected_clients_count')}, Radio settings type: {type(device.get('radio_settings')).__name__}"
        # ) # Corrected: Removed stray parenthesis here

    async def _async_get_camera_video_settings(self, device: Dict[str, Any]) -> None:
        """Fetch and store video settings (specifically externalRtspEnabled and rtspUrl) for a camera device.

        Updates the `device` dictionary in-place. Handles API errors by logging
        and ensuring `externalRtspEnabled` and `rtspUrl` are None if fetch fails.

        Args:
            device: The camera device dictionary to update. Must contain 'serial'.
        """
        serial = device.get("serial")
        if not serial:  # Should be caught by caller, but good practice
            _LOGGER.warning(
                "Cannot fetch camera video settings: device serial is missing."
            )
            device["externalRtspEnabled"] = None
            device["rtspUrl"] = None
            return

        # externalRtspEnabled and rtspUrl should have been initialized to None by the caller.
        async with self._api_call_semaphore:
            video_settings = await self._async_meraki_api_call(
                self.meraki_client.camera.getDeviceCameraVideoSettings(
                    serial=serial
                ),  # Use self.meraki_client
                f"getDeviceCameraVideoSettings(serial={serial})",
            )

        if video_settings is not None:
            external_rtsp_enabled = video_settings.get("externalRtspEnabled")
            rtsp_url = video_settings.get("rtspUrl")
            device["externalRtspEnabled"] = external_rtsp_enabled
            device["rtspUrl"] = rtsp_url
            # _LOGGER.debug(
            #     f"Fetched video settings for camera {serial}. externalRtspEnabled: {external_rtsp_enabled}, rtspUrl: {rtsp_url}"
            # )
        else:
            _LOGGER.warning(
                f"Could not fetch video settings for camera {serial}. externalRtspEnabled and rtspUrl will remain None."
            )

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        call_description = f"getOrganizationNetworks(organizationId={org_id})"
        org_networks = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationNetworks(
                organizationId=org_id
            ),
            call_description,
        )

        if org_networks is None:  # API call failed or returned None (handled by helper)
            _LOGGER.warning(
                f"{call_description} returned None or failed."
            )  # Helper already logs specifics
            return None
        if not org_networks:  # Empty list is a valid response
            _LOGGER.info(
                f"No networks found for organization ID {org_id}."
            )  # Changed from warning to info
            # Depending on strictness, could return [] directly if that's preferred over None for "empty"
            return []

        # _LOGGER.debug(
        #     f"Successfully fetched {len(org_networks)} networks for org ID {org_id}."
        # ) # Reduced verbosity
        return org_networks

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK."""
        call_description = f"getOrganizationDevices(organizationId={org_id})"
        devices_data = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationDevices(
                organizationId=org_id
            ),
            call_description,
        )

        if devices_data is None:
            _LOGGER.warning(f"{call_description} returned None or failed.")
            return None
        if not devices_data:
            _LOGGER.info(f"No devices found for organization ID {org_id}.")
            return []

        # _LOGGER.debug(
        #     f"Received {len(devices_data)} devices from SDK for org {org_id}."
        # ) # Reduced verbosity
        return devices_data

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK."""
        call_description = f"getNetworkWirelessSsids(networkId={network_id})"
        async with self._api_call_semaphore:
            ssids_data = await self._async_meraki_api_call(
                self.meraki_client.wireless.getNetworkWirelessSsids(networkId=network_id),
                call_description,
                return_empty_list_on_404=True,  # Specific for SSIDs, as 404 means no wireless capability / no SSIDs
            )

        # If ssids_data is None, it means a non-404 error occurred.
        # If it's an empty list, it means either a 404 occurred and was handled, or the API returned an empty list (no SSIDs).
        if ssids_data is None:
            _LOGGER.warning(
                f"{call_description} failed with a non-404 error. SSIDs for this network will be unavailable."
            )
            return None  # Critical error, not just "no SSIDs"

        # If ssids_data is an empty list (either from 404 or actual empty response), log appropriately.
        if not ssids_data:
            _LOGGER.info(
                f"No SSIDs found or network does not support SSIDs (network ID: {network_id})."
            )
            return []  # Return empty list, consistent

        return ssids_data

    async def _async_get_mx_device_uplink_settings(
        self, device: Dict[str, Any]
    ) -> None:
        """Fetch and store WAN DNS server settings from uplink configuration for an MX (appliance) device.

        This method updates the provided `device` dictionary in-place with
        `wan1_dns_servers` and `wan2_dns_servers`. It attempts to parse these
        from the device's uplink settings API response. Handles API errors
        gracefully by logging warnings and ensuring default empty lists.

        Args:
            device: The device dictionary to update. Must contain 'serial'.
        """
        serial = device.get("serial")
        if not serial:
            _LOGGER.warning(
                "Cannot fetch uplink settings for MX device: missing serial. Device data: %s",
                str(device)[:100],
            )
            device["wan1_dns_servers"] = []
            device["wan2_dns_servers"] = []
            return

        # _LOGGER.debug(
        #     f"Fetching uplink settings for MX device {device.get('name', 'Unknown')} (Serial: {serial})"
        # ) # Reduced verbosity

        async with self._api_call_semaphore:
            uplink_settings = await self._async_meraki_api_call(
                self.meraki_client.appliance.getDeviceApplianceUplinksSettings(
                    serial=serial
                ),  # Use self.meraki_client
                f"getDeviceApplianceUplinksSettings(serial={serial})",
            )

        try:
            interfaces_data = (
                uplink_settings.get("interfaces", {}) if uplink_settings else {}
            )

            for wan_key in ["wan1", "wan2"]:  # Potentially more like "cellular", etc.
                interface_specific_settings = interfaces_data.get(wan_key, {})
                dns_servers = self._extract_dns_servers_for_wan(
                    interface_name=wan_key,
                    interface_api_settings=interface_specific_settings,
                    device_global_data=device,
                )
                device[f"{wan_key}_dns_servers"] = dns_servers
                # _LOGGER.debug(
                #     f"Populated {wan_key}_dns_servers for {serial}: {dns_servers}"
                # ) # Reduced verbosity

            if not uplink_settings:
                # _LOGGER.debug(
                #     f"Uplink settings data was None for MX device {device.get('name', 'Unknown')} (Serial: {serial}) (API call failed or returned no data). "
                #     "Attempting device-level fallbacks for DNS."
                # ) # Reduced verbosity
                pass # Fallback will handle

            for wan_key in ["wan1", "wan2"]:
                interface_specific_settings = interfaces_data.get(wan_key, {})
                dns_servers = self._extract_dns_servers_for_wan(
                    interface_name=wan_key,
                    interface_api_settings=interface_specific_settings,
                    device_global_data=device,
                )
                if dns_servers:
                    device[f"{wan_key}_dns_servers"] = dns_servers
                elif f"{wan_key}_dns_servers" not in device:
                    device[f"{wan_key}_dns_servers"] = []

        except Exception as e:
            _LOGGER.exception(
                f"Unexpected error processing uplink settings for MX device {device.get('name', 'Unknown')} (Serial: {serial}): {e}. "
                "Ensuring DNS keys exist with fallback."
            )
            for wan_key in ["wan1", "wan2"]:
                if f"{wan_key}_dns_servers" not in device:
                    device[f"{wan_key}_dns_servers"] = self._extract_dns_servers_for_wan(
                        interface_name=wan_key,
                        interface_api_settings={},
                        device_global_data=device,
                        force_device_fallback_check=True,
                    )
                    # _LOGGER.debug(
                    #     f"Ensured {wan_key}_dns_servers for {serial} after processing error: {device[f'{wan_key}_dns_servers']}"
                    # ) # Reduced verbosity

    def _extract_dns_servers_for_wan(
        self,
        interface_name: str,
        interface_api_settings: Dict[str, Any],
        device_global_data: Dict[str, Any],
        force_device_fallback_check: bool = False,
    ) -> List[str]:
        """Helper to extract DNS servers for a specific WAN interface using multiple fallbacks."""
        current_wan_dns_ips = []

        # 1. Primary: 'svis' -> 'ipv4' -> 'nameservers' (from specific interface API settings)
        if (
            not force_device_fallback_check
        ):  # Only try API data if not forced to skip to device global
            svis_data = interface_api_settings.get("svis")
            if isinstance(svis_data, dict):
                ipv4_data = svis_data.get("ipv4")
                if isinstance(ipv4_data, dict):
                    nameservers_list = ipv4_data.get("nameservers")
                    if isinstance(nameservers_list, list):
                        for ns_entry in nameservers_list:
                            if isinstance(ns_entry, dict) and isinstance(
                                ns_entry.get("addresses"), list
                            ):
                                for ip_addr in ns_entry.get("addresses", []):
                                    if (
                                        isinstance(ip_addr, str)
                                        and ip_addr not in current_wan_dns_ips
                                    ):
                                        current_wan_dns_ips.append(ip_addr)

            if current_wan_dns_ips:  # Found via primary API method
                return current_wan_dns_ips

            # 2. Fallback: 'dnsServers' directly under interface_settings (from specific interface API settings)
            dns_servers_field = interface_api_settings.get("dnsServers")
            if isinstance(dns_servers_field, list):
                for dns_entry in dns_servers_field:
                    if isinstance(dns_entry, str) and (
                        "." in dns_entry or ":" in dns_entry
                    ):
                        if dns_entry not in current_wan_dns_ips:
                            current_wan_dns_ips.append(dns_entry)
            elif isinstance(dns_servers_field, str) and (
                "." in dns_servers_field or ":" in dns_servers_field
            ):
                if dns_servers_field not in current_wan_dns_ips:
                    current_wan_dns_ips.append(dns_servers_field)

            if current_wan_dns_ips:  # Found via secondary API method
                return current_wan_dns_ips

        # 3. Second Fallback: Device-level fields like 'wan1PrimaryDns' (from global device data)
        # This part is crucial if API data is missing/empty or if force_device_fallback_check is True
        primary_dns_key = f"{interface_name}PrimaryDns"
        secondary_dns_key = f"{interface_name}SecondaryDns"

        primary_dns = device_global_data.get(primary_dns_key)
        if (
            primary_dns
            and isinstance(primary_dns, str)
            and primary_dns not in current_wan_dns_ips
        ):
            current_wan_dns_ips.append(primary_dns)

        secondary_dns = device_global_data.get(secondary_dns_key)
        if (
            secondary_dns
            and isinstance(secondary_dns, str)
            and secondary_dns not in current_wan_dns_ips
        ):
            current_wan_dns_ips.append(secondary_dns)

        return current_wan_dns_ips

    async def _async_get_mx_lan_dns_settings(self, device: Dict[str, Any]) -> None:
        """Fetch and store LAN DNS settings from VLAN configurations for an MX (appliance) device.

        This method updates the provided `device` dictionary in-place with
        `lan_dns_settings`, a dictionary mapping VLAN names/IDs to their
        DNS configurations (e.g., "google_dns", "opendns", or a list of custom IPs).
        Handles API errors gracefully.

        Args:
            device: The device dictionary to update. Must contain 'networkId' and 'serial'.
        """
        network_id = device.get("networkId")
        serial = device.get("serial", "N/A")  # For logging
        device_name = device.get("name", "Unknown")  # For logging

        if not network_id or not isinstance(network_id, str):
            _LOGGER.warning(
                f"Cannot fetch LAN DNS settings for MX device {device_name} (Serial: {serial}): 'networkId' is missing or invalid (type: {type(network_id).__name__})."
            )
            device["lan_dns_settings"] = {}
            return

        # _LOGGER.debug(
        #     f"Fetching LAN DNS (VLAN settings) for MX device {device_name} (Serial: {serial}, Network: {network_id})"
        # ) # Reduced verbosity

        lan_dns_by_vlan: Dict[str, Any] = {}
        vlan_list_to_iterate: List[Dict[str, Any]] = []

        try:
            async with self._api_call_semaphore:
                vlan_settings_response = await self._async_meraki_api_call(
                    self.meraki_client.appliance.getNetworkApplianceVlansSettings(
                        networkId=network_id
                    ),  # Use self.meraki_client
                    f"getNetworkApplianceVlansSettings(networkId={network_id})",
                    return_empty_list_on_404=True,
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
                            # _LOGGER.debug(
                            #     f"VLAN {vlan_key} on {serial} using custom DNS: {custom_dns_servers}"
                            # ) # Removed: too verbose
                        else:  # If set to "custom_servers" but no IPs are listed.
                            lan_dns_by_vlan[vlan_key] = []  # Store as empty list.
                            _LOGGER.debug(
                                f"VLAN {vlan_key} on {serial} set to 'custom_servers' but no IPs provided."
                            )
                    elif (
                        dns_nameservers_setting
                    ):  # If not "custom_servers", store the setting string itself (e.g., "google_dns").
                        lan_dns_by_vlan[vlan_key] = dns_nameservers_setting
                        # _LOGGER.debug(
                        #     f"VLAN {vlan_key} on {serial} using preset DNS: {dns_nameservers_setting}"
                        # ) # Removed: too verbose
                    else:  # If no specific DNS setting ('dnsNameservers') found for the VLAN.
                        lan_dns_by_vlan[vlan_key] = (
                            "Not configured"  # Indicate not configured.
                        )
                        _LOGGER.debug(
                            f"VLAN {vlan_key} on {serial} has no explicit DNS configuration."
                        )
            # If vlan_list_to_iterate is empty (e.g., from None response or unexpected type), this loop is skipped.

        except MerakiSDKAPIError:
            if vlan_settings_response is None:
                _LOGGER.warning(
                    f"LAN DNS settings could not be fetched for MX device {device_name} (Serial: {serial}, Network: {network_id})."
                )

        except Exception as e:
            _LOGGER.exception(
                f"Unexpected error structure in _async_get_mx_lan_dns_settings for {device_name} (Serial: {serial}, Network: {network_id}): {e}."
            )

        # Store the collected LAN DNS settings in the main device dictionary.
        device["lan_dns_settings"] = lan_dns_by_vlan
        _LOGGER.debug(
            f"Final LAN DNS settings for {device_name} (Serial: {serial}): {lan_dns_by_vlan}"
        )
