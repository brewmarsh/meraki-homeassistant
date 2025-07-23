"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices (including tags), SSIDs, and device-specific details
like client counts and radio settings for MR devices, using the Meraki SDK.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Awaitable, Tuple  # Added Tuple

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
        self._api_call_semaphore = asyncio.Semaphore(
            5
        )  # Allow up to 5 concurrent API calls
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
            self._async_meraki_api_call(
                self.meraki_client.organizations.getOrganizations(),
                "getOrganizations",
            ),
            self.async_get_networks(self.org_id),
            self.async_get_organization_devices(self.org_id),
            self._async_meraki_api_call(
                self.meraki_client.organizations.getOrganizationDevicesStatuses(
                    organizationId=self.org_id, total_pages="all"
                ),
                "getOrganizationDevicesStatuses",
            ),
            self._async_meraki_api_call(
                self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                    organizationId=self.org_id
                ),
                "getOrganizationFirmwareUpgrades",
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
                _LOGGER.warning(
                    "Device %s (MAC: %s, Model: %s) has no serial number. This may be a temporary issue or the device may not be fully claimed. Skipping additional detail tasks.",
                    device.get("name", "N/A"),
                    device.get("mac", "N/A"),
                    device_model,
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
                            latest_item_version_val = to_version_info.get(
                                "version", "N/A"
                            )
                            if latest_item_version_val:
                                latest_item_version = latest_item_version_val
                            else:
                                pass
                            is_item_up_to_date = False
                        else:
                            if to_version_info is not None:
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
                                        latest_item_version_val = available_versions[
                                            0
                                        ].get("version", "N/A")
                                        if latest_item_version_val:
                                            latest_item_version = (
                                                latest_item_version_val
                                            )
                                    else:
                                        _LOGGER.warning(
                                            "First item in 'availableVersions' for serial %s is not a dict: %s. Cannot determine latest available version.",
                                            item_serial,
                                            str(available_versions[0])[:100],
                                        )
                                elif available_versions is not None:
                                    _LOGGER.warning(
                                        "'availableVersions' for serial %s is not a non-empty list: %s. Cannot determine latest available version.",
                                        item_serial,
                                        str(available_versions)[:100],
                                    )
                    elif next_upgrade_info is not None:
                        _LOGGER.warning(
                            "Firmware upgrade item for serial %s has 'nextUpgrade' but it's not a dictionary: %s.",
                            item_serial,
                            str(next_upgrade_info)[:100],
                        )
                        item_status = str(upgrade_item.get("status", "")).lower()
                        if item_status == "up-to-date":
                            is_item_up_to_date = True
                        elif item_status == "has-newer-stable-version":
                            is_item_up_to_date = False
                            available_versions = upgrade_item.get("availableVersions")
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
                        item_status = str(
                            upgrade_item.get("status", "")
                        ).lower()  # All on one line
                        if item_status == "up-to-date":
                            is_item_up_to_date = True
                        elif upgrade_item.get("latestVersion"):
                            latest_item_version_val = upgrade_item.get("latestVersion")
                            if latest_item_version_val:
                                latest_item_version = latest_item_version_val
                        elif item_status == "has-newer-stable-version":
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
                latest_known_version = (
                    current_device_firmware if current_device_firmware else "N/A"
                )

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
                        latest_known_version = (
                            current_device_firmware
                            if current_device_firmware
                            else "N/A"
                        )
                    elif api_latest_version and api_latest_version != "N/A":
                        latest_known_version = api_latest_version
                        if (
                            current_device_firmware
                            and current_device_firmware == latest_known_version
                        ):
                            is_up_to_date_bool = True
                        else:
                            is_up_to_date_bool = False
                    elif api_reported_up_to_date:
                        is_up_to_date_bool = True
                        latest_known_version = (
                            current_device_firmware
                            if current_device_firmware
                            else "N/A"
                        )
                    else:
                        is_up_to_date_bool = False
                        if api_latest_version and api_latest_version != "N/A":
                            latest_known_version = api_latest_version

                    if (
                        current_device_firmware
                        and current_device_firmware == latest_known_version
                    ):
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
        ssid_tasks = []
        if networks:
            for network in networks:
                network_id = network.get("id")
                if not network_id:
                    continue
                ssid_tasks.append(self.async_get_network_ssids(network_id))
            if ssid_tasks:
                results = await asyncio.gather(*ssid_tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, list):
                        ssids.extend(result)
                    elif isinstance(result, Exception):
                        _LOGGER.error(
                            "Meraki SDK API error fetching SSIDs for a network: %s",
                            result,
                        )

        # Step 7: Fetch all clients across all networks.
        all_clients: List[Dict[str, Any]] = []
        client_tasks = []
        if networks:
            for network in networks:
                network_id = network.get("id")
                if not network_id:
                    continue
                client_tasks.append(
                    self._async_meraki_api_call(
                        self.meraki_client.networks.getNetworkClients(
                            network_id, timespan=3600
                        ),
                        f"getNetworkClients(networkId={network_id})",
                        return_empty_list_on_404=True,
                    )
                )
            if client_tasks:
                results = await asyncio.gather(*client_tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, list):
                        all_clients.extend(result)
                    elif isinstance(result, Exception):
                        _LOGGER.error(
                            "Meraki SDK API error fetching clients for a network: %s",
                            result,
                        )
        # Step 8: Prepare device type mapping and aggregate client counts
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

        # Initialize client count variables
        clients_on_ssids = 0
        clients_on_wireless = 0
        clients_on_appliances = 0

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
        self, api_coro: Awaitable[Any], call_description: str, return_empty_list_on_404: bool = False
    ) -> Optional[Any]:
        """Wrapper for Meraki API calls with error handling.

        Args:
            api_coro: The API coroutine to execute.
            call_description: A string describing the API call for logging purposes.
            return_empty_list_on_404: If True, return [] on 404 errors.

        Returns:
            The API response, an empty list on 404 if specified, or None on other errors.
        """
        try:
            async with self._api_call_semaphore:
                return await api_coro
        except MerakiSDKAPIError as e:
            if hasattr(e, "status") and e.status == 404:
                if return_empty_list_on_404:
                    _LOGGER.info(
                        "Meraki API call '%s' returned 404, handled as empty list.",
                        call_description,
                    )
                    return []
                else:
                    _LOGGER.warning(
                        "Meraki API call '%s' returned 404, but not handled as empty list. Returning None.",
                        call_description,
                    )
                    return None
            _LOGGER.error(
                "Meraki SDK API error during '%s' for org %s: %s. Status: %s, Reason: %s.",
                call_description,
                self.org_id,
                e,
                e.status,
                e.reason,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error during '%s' for org %s: %s",
                call_description,
                self.org_id,
                e,
            )
            return None
        _LOGGER.debug(f"Fetching all data for organization ID: {self.org_id} using SDK")

        try:
            # Fetch organization info first
            org_info = await self.meraki_client.organizations.getOrganization(
                organizationId=self.org_id
            )

            # Fetch networks
            networks_data = (
                await self._async_meraki_api_call(
                    self.meraki_client.organizations.getOrganizationNetworks(
                        organizationId=self.org_id
                    ),
                    return_empty_list_on_404=True,
                )
                or []
            )

            # Process networks and devices
            processed_devices = []
            for network in networks_data:
                network_id = network.get("id")
                if not network_id:
                    _LOGGER.warning("Found network without ID, skipping: %s", network)
                    continue

                # Fetch network-specific data
                try:
                    network_devices = (
                        await self._async_meraki_api_call(
                            self.meraki_client.networks.getNetworkDevices(
                                networkId=network_id
                            ),
                            return_empty_list_on_404=True,
                        )
                        or []
                    )

                    for device in network_devices:
                        if not _is_valid_device(device):
                            _log_skipped_device(device, "missing required attributes")
                            if isinstance(device, dict):
                                device["is_incomplete"] = True
                                processed_devices.append(device)
                            continue

                        processed_devices.append(device)

                except Exception as e:
                    _LOGGER.error(
                        "Error fetching devices for network %s: %s", network_id, str(e)
                    )

            return {
                "org_name": org_info.get("name"),
                "networks": networks_data,
                "devices": processed_devices,
                "ssids": [],  # Will be populated by SSID fetching logic
                "clients": [],  # Will be populated by client fetching logic
            }

        except Exception as e:
            _LOGGER.exception("Critical error fetching organization data: %s", str(e))
            raise UpdateFailed(
                f"Failed to fetch critical organization data: {str(e)}"
            ) from e

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

        video_settings = await self._async_meraki_api_call(
            self.meraki_client.camera.getDeviceCameraVideoSettings(serial=serial),
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
        org_networks = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationNetworks(organizationId=org_id),
            f"getOrganizationNetworks(organizationId={org_id})",
            return_empty_list_on_404=True,
        )

        if org_networks is None:
            _LOGGER.warning(
                f"getOrganizationNetworks(organizationId={org_id}) returned None or failed."
            )
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
        devices_data = await self._async_meraki_api_call(
            self.meraki_client.organizations.getOrganizationDevices(organizationId=org_id),
            f"getOrganizationDevices(organizationId={org_id})",
            return_empty_list_on_404=True,
        )

        if devices_data is None:
            _LOGGER.warning(
                f"getOrganizationDevices(organizationId={org_id}) returned None or failed."
            )
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
        ssids_data = await self._async_meraki_api_call(
            self.meraki_client.wireless.getNetworkWirelessSsids(networkId=network_id),
            f"getNetworkWirelessSsids(networkId={network_id})",
            return_empty_list_on_404=True,
        )

        if ssids_data is None:
            _LOGGER.warning(
                f"getNetworkWirelessSsids(networkId={network_id}) returned None or failed."
            )
            return None
        if not ssids_data:
            _LOGGER.info(
                f"No SSIDs found for network ID {network_id}."
            )  # Changed from warning to info
            return []

        # _LOGGER.debug(
        #     f"Successfully fetched {len(ssids_data)} SSIDs for network ID {network_id}."
        # ) # Reduced verbosity
        return ssids_data

    async def process_clients(
        self,
        all_clients: List[Dict[str, Any]],
        device_serial_to_type_map: Dict[str, str],
    ) -> Tuple[int, int, int]:
        """Process client data and calculate client counts.

        Args:
            all_clients: List of client dictionaries
            device_serial_to_type_map: Mapping of device serials to their types

        Returns:
            Tuple of (clients_on_ssids, clients_on_appliances, clients_on_wireless)
        """
        clients_on_ssids = 0
        clients_on_appliances = 0
        clients_on_wireless = 0

        for client_idx, client in enumerate(all_clients):
            if not isinstance(client, dict):
                _LOGGER.warning(
                    "Skipping non-dictionary client at index %d: %s",
                    client_idx,
                    str(client)[:100],
                )
                continue

            if client.get("ssid"):
                clients_on_ssids += 1

            ap_serial = client.get("recentDeviceSerial") or client.get("deviceSerial")
            if ap_serial and ap_serial in device_serial_to_type_map:
                device_type = device_serial_to_type_map[ap_serial]
                if device_type == "Wireless":
                    clients_on_wireless += 1
                elif device_type == "Appliance":
                    clients_on_appliances += 1

        return clients_on_ssids, clients_on_appliances, clients_on_wireless

    async def process_org_details(self) -> Optional[str]:
        """Fetch and process organization details.

        Returns:
            Organization name if successful, None otherwise
        """
        try:
            org_details = await self.meraki_client.organizations.getOrganization(
                organizationId=self.org_id
            )
            if org_details and isinstance(org_details, dict):
                org_name = org_details.get("name")
                if not org_name:
                    _LOGGER.warning(
                        "Organization details retrieved but name is missing for org %s",
                        self.org_id,
                    )
                return org_name
            else:
                _LOGGER.warning(
                    "Organization details response was not a dictionary for org %s: %s",
                    self.org_id,
                    str(org_details)[:100],
                )
                return None
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                "Meraki API error fetching organization details for org %s: %s. Status: %s",
                self.org_id,
                str(e),
                getattr(e, "status", "Unknown"),
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching organization details for org %s: %s",
                self.org_id,
                str(e),
            )
            return None


def _is_network_feature_not_found(error: MerakiSDKAPIError) -> bool:
    """Determine if the error is due to a network feature not being found.

    Args:
        error: The MerakiSDKAPIError instance to check.

    Returns:
        True if the error indicates a network feature not found, False otherwise.
    """
    # Check if the error message or reason indicates a feature not found scenario
    return (
        error.status == 404
        and "not found" in (error.reason or "").lower()
        and "feature" in (error.message or "").lower()
    )


def _is_valid_device(device: Dict[str, Any]) -> bool:
    """Check if the device dictionary has all required attributes.

    Args:
        device: The device dictionary to check.

    Returns:
        True if the device is valid, False otherwise.
    """
    required_attributes = ["serial", "model", "mac", "name"]
    return all(
        attr in device and device[attr] is not None for attr in required_attributes
    )


def _log_skipped_device(device: Dict[str, Any], reason: str) -> None:
    """Log a skipped device due to missing attributes or other issues.

    Args:
        device: The device dictionary that was skipped.
        reason: The reason why the device was skipped.
    """
    _LOGGER.info(
        "Skipping device %s (Serial: %s, MAC: %s) - %s",
        device.get("name", "Unknown"),
        device.get("serial", "Unknown"),
        device.get("mac", "Unknown"),
        reason,
    )
