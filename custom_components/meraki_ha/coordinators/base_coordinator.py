"""Base data update coordinator for the Meraki Home Assistant integration.

This module defines `MerakiDataUpdateCoordinator`, the primary coordinator
responsible for orchestrating data fetching and updates from the Meraki API.
It uses `MerakiApiDataFetcher` to retrieve all data (networks, devices with
tags, SSIDs, etc.) and `DataAggregationCoordinator` to process this data into
a unified structure for the integration. It also manages optional tag erasing
via `TagEraserCoordinator`.
"""

import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from custom_components.meraki_ha.const import DOMAIN, ERASE_TAGS_WARNING
from custom_components.meraki_ha.coordinators.api_data_fetcher import (
    MerakiApiDataFetcher,
)

# MerakiApiError for exception handling
from custom_components.meraki_ha.meraki_api import MerakiApiError
from custom_components.meraki_ha.coordinators.data_aggregation_coordinator import (
    DataAggregationCoordinator,
)

# Added imports for device registration
from homeassistant.helpers import device_registry as dr
from .meraki_device_types import map_meraki_model_to_device_type


# Obsolete coordinators (DeviceTagFetchCoordinator,
# MerakiNetworkCoordinator, MerakiSsidCoordinator) removed.
from custom_components.meraki_ha.coordinators.tag_eraser_coordinator import (
    TagEraserCoordinator,
)

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Manages fetching and processing of Meraki data for Home Assistant.

    This coordinator orchestrates the overall data flow:
    1. Uses `MerakiApiDataFetcher` to fetch all required data from the Meraki API
       (networks, devices including tags, SSIDs, client counts for MRs, etc.).
    2. Passes the fetched data to `DataAggregationCoordinator` which processes
       and structures it.
    3. If configured, uses `TagEraserCoordinator` to remove specified tags
       from devices.
    The resulting aggregated data is stored in `self.data` for HASS entities.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        relaxed_tag_match: bool,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki data update coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval at which to periodically update data.
            relaxed_tag_match: Boolean indicating if relaxed tag matching
                               should be used for SSID status calculation.
            config_entry: The config entry associated with this coordinator instance.
        """
        self.api_key: str = api_key  # Stored for potential direct use (e.g., TagEraser)
        self.org_id: str = org_id
        self.config_entry: ConfigEntry = config_entry  # Access to options, entry_id
        self.relaxed_tag_match: bool = relaxed_tag_match
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        # Initialize the MerakiAPIClient for SDK interactions.
        # This client is passed to the api_fetcher and its lifecycle managed
        # here.
        # Local import to avoid potential circulars
        from custom_components.meraki_ha.meraki_api import MerakiAPIClient

        self.meraki_client: MerakiAPIClient = MerakiAPIClient(
            api_key=api_key,
            org_id=org_id,
            # Base URL is handled by the SDK itself.
        )

        # Initialize the main API data fetcher.
        self.api_fetcher: MerakiApiDataFetcher = MerakiApiDataFetcher(
            meraki_client=self.meraki_client
        )

        # Initialize the DataAggregationCoordinator.
        # This sub-coordinator processes data fetched by api_fetcher.
        self.data_aggregation_coordinator: DataAggregationCoordinator = (
            DataAggregationCoordinator(
                hass,
                scan_interval,
                # scan_interval passed for consistency, though DAC updates on
                # demand.
                relaxed_tag_match,
                self,  # Pass self as parent coordinator for context.
            )
        )

        # Initialize TagEraserCoordinator if tag erasing is enabled.
        self.tag_eraser_coordinator: Optional[TagEraserCoordinator] = None
        if self.erase_tags:
            self.tag_eraser_coordinator = TagEraserCoordinator(
                hass,
                api_key,
                # TagEraser might need direct API key for write operations.
                org_id,
            )
            _LOGGER.warning(ERASE_TAGS_WARNING)

        # `self.device_data` will store the list of devices after fetching.
        # This is primarily for internal use before aggregation or for tag
        # erasing.
        self.device_data: List[Dict[str, Any]] = []
        # Obsolete comments for self.ssid_data and self.network_data removed.

        # Call superclass constructor to set up periodic updates.
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} (Org: {org_id})",  # More descriptive name.
            update_interval=scan_interval,
        )
        # Ensure `self.data` is initialized to an empty dict, as expected by
        # DataUpdateCoordinator.
        self.data: Dict[str, Any] = {}

    @property
    def device_name_format(self) -> str:
        """Return the device name format option."""
        return self.config_entry.options.get("device_name_format", "omitted")

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch, process, and aggregate data from the Meraki API.

        This is the core method called periodically by the DataUpdateCoordinator.
        It orchestrates the entire data refresh cycle:
        1. Fetches all raw data (networks, devices with tags, SSIDs, etc.) using `api_fetcher`.
        2. Passes this raw data to `data_aggregation_coordinator` for processing and structuring.
        3. If tag erasing is enabled, iterates through devices and calls `tag_eraser_coordinator`.
        The final, aggregated data is returned and stored in `self.data`.

        Returns:
            A dictionary containing the fully processed and aggregated data for the integration.

        Raises:
            UpdateFailed: If a critical error occurs during data fetching or processing
                          that prevents a meaningful update for the integration.
        """
        _LOGGER.debug(
            "Starting Meraki data update for organization ID: %s", self.org_id
        )
        try:
            # Step 1: Fetch all primary data using the api_fetcher.
            # `fetch_all_data` now returns devices with tags, client counts, and radio settings included.
            all_data: Dict[str, Any] = await self.api_fetcher.fetch_all_data(
                self.hass,
                # Other arguments like org_id, scan_interval,
                # device_name_format are no longer needed here.
            )
        except MerakiApiError as e:  # Specific API errors from the fetcher.
            _LOGGER.error(
                "API error during Meraki data fetch for org %s: %s", self.org_id, e
            )
            raise UpdateFailed(
                f"Failed to fetch data from Meraki API for org {self.org_id}: {e}"
            ) from e
        except (
            Exception
        ) as e:  # Catch any other unexpected errors during the main fetch.
            _LOGGER.exception(
                "Unexpected error during Meraki data fetch for org %s: %s",
                self.org_id,
                e,
            )
            raise UpdateFailed(
                f"Unexpected error fetching data for org {self.org_id}: {e}"
            ) from e

        # Extract data components from `all_data`. Default to empty lists if
        # keys are missing.
        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])
        clients_list: List[Dict[str, Any]] = all_data.get(
            "clients", []
        )  # New: Extract clients

        # Step 2: Device tags are now part of the `devices` list from `all_data`.
        # No separate tag fetching step is needed here.

        # Step 3: Obsolete step for updating separate network/SSID coordinators removed.
        # Data is passed directly to the DataAggregationCoordinator.

        # Store the fetched devices list internally. This list includes tags
        # and MR-specific details.
        self.device_data = devices

        # ---- START NETWORK DEVICE REGISTRATION LOGIC ----
        _LOGGER.debug(
            "Starting Meraki Network device registration process for org %s.",
            self.org_id,
        )
        device_registry = dr.async_get(self.hass)  # Ensure dr is available
        processed_network_devices = 0
        for network_info in networks:  # 'networks' is all_data.get("networks", [])
            network_id = network_info.get("id")
            network_name = network_info.get("name")

            if not network_id:
                _LOGGER.warning(
                    "Found a network with missing ID, cannot register as HA device: %s",
                    network_info,
                )
                continue
            if not network_name:  # Fallback name if network name is missing
                original_network_name = f"Meraki Network {network_id}"
                _LOGGER.warning(
                    "Found network with missing name (ID: %s), using fallback name: %s",
                    network_id,
                    original_network_name,
                )
            else:
                original_network_name = network_name

            # Apply device_name_format for Network devices
            # self.device_name_format is a property that gets it from config_entry.options
            current_device_name_format = self.device_name_format

            formatted_network_name = original_network_name
            if current_device_name_format == "prefix":
                formatted_network_name = f"[Network] {original_network_name}"
            elif current_device_name_format == "suffix":
                formatted_network_name = f"{original_network_name} [Network]"
            # If "omitted" or other, use original_network_name as is

            _LOGGER.debug(
                "Registering Meraki Network device: %s (ID: %s), Format: %s",
                formatted_network_name,
                network_id,
                current_device_name_format,
            )
            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={
                    (DOMAIN, network_id)
                },  # Unique identifier for this network device
                name=formatted_network_name,  # Use the formatted name
                model="Meraki Network",  # Model for these logical network devices
                manufacturer="Cisco Meraki",
                # No via_device for these, they are parented by the ConfigEntry implicitly
            )
            processed_network_devices += 1
        _LOGGER.debug(
            "Processed %d Meraki Network devices for registration for org %s.",
            processed_network_devices,
            self.org_id,
        )
        # ---- END NETWORK DEVICE REGISTRATION LOGIC ----

        # ---- START PHYSICAL DEVICE REGISTRATION LOGIC ----
        _LOGGER.debug(
            "Starting physical device registration process for org %s.", self.org_id
        )
        # device_registry instance is already available from network registration part

        for device_info in devices:  # 'devices' is all_data.get("devices", [])
            serial = device_info.get("serial")
            if not serial:
                _LOGGER.warning(
                    "Device found without serial, cannot register: %s", device_info
                )
                continue

            device_name_raw = device_info.get("name") or serial
            device_model_str = device_info.get("model", "Unknown")
            firmware_version = device_info.get("firmware")  # Get firmware version here

            # Standard mapping for physical devices processed by this coordinator.
            # The placeholder conditions for "SSID" and "Network" types have been removed
            # as they do not apply to the physical devices (APs, switches, gateways, etc.)
            # processed in this loop. SSID-specific naming is handled in SSIDDeviceCoordinator.
            # map_meraki_model_to_device_type provides the correct type (e.g., "Wireless", "Switch", "Appliance").
            device_type_mapped = map_meraki_model_to_device_type(device_model_str)

            formatted_device_name = device_name_raw
            # Use the property self.device_name_format
            if self.device_name_format == "prefix" and device_type_mapped != "Unknown":
                formatted_device_name = f"[{device_type_mapped}] {device_name_raw}"
            elif (
                self.device_name_format == "suffix" and device_type_mapped != "Unknown"
            ):
                formatted_device_name = f"{device_name_raw} [{device_type_mapped}]"

            # Prepare connections set using MAC address
            mac_address = device_info.get("mac")
            connections = None
            if mac_address:
                connections = {(dr.CONNECTION_NETWORK_MAC, mac_address)}

            # Log the full device_info for debugging before registration attempt
            # This log was already added in a previous step, ensuring it's correctly placed.
            # _LOGGER.debug(
            #     "MERAKI_DEBUG_COORDINATOR: Preparing to register/update physical device. Full device_info: %s",
            #     device_info
            # )

            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, serial)},
                manufacturer="Cisco Meraki",
                model=device_model_str,
                name=formatted_device_name,
                sw_version=firmware_version,  # firmware_version from device_info.get("firmware")
                connections=connections,  # Pass the connections set
            )
            _LOGGER.debug(
                "Registered/Updated physical device: %s (Serial: %s, Model: %s, MAC: %s, FW: %s, Status: %s)",
                formatted_device_name,
                serial,
                device_model_str,
                mac_address or "N/A",  # Log MAC address
                firmware_version or "N/A",  # Log firmware version
                device_info.get("status", "N/A"),  # Log status
            )
        _LOGGER.debug("Device registration process completed for org %s.", self.org_id)
        # ---- END DEVICE REGISTRATION LOGIC ----

        # Process client data to get network client counts
        from custom_components.meraki_ha.coordinators.data_processor import (
            MerakiDataProcessor,
        )  # Ensure import

        processor = MerakiDataProcessor(self)  # Instantiate processor
        network_client_counts = processor.process_network_client_counts(clients_list)

        # Extract the new organization-wide client counts from all_data
        clients_on_ssids = all_data.get("clients_on_ssids", 0)
        clients_on_appliances = all_data.get("clients_on_appliances", 0)
        clients_on_wireless = all_data.get("clients_on_wireless", 0)

        # Step 4: Aggregate all data using the DataAggregationCoordinator.
        # This coordinator takes the raw lists of devices, SSIDs, and networks.
        try:
            combined_data: Dict[str, Any] = (
                await self.data_aggregation_coordinator._async_update_data(
                    devices,  # Pass the comprehensive devices list.
                    ssids,  # Pass the SSIDs list.
                    networks,  # Pass the networks list.
                    clients_list,
                    network_client_counts,
                    clients_on_ssids=clients_on_ssids,
                    clients_on_appliances=clients_on_appliances,
                    clients_on_wireless=clients_on_wireless,
                    # The fourth `device_tags` argument has been removed from
                    # _async_update_data.
                )
            )
        except Exception as e:  # Catch errors specifically from the aggregation step.
            _LOGGER.exception(
                "Error during data aggregation for org %s: %s", self.org_id, e
            )
            raise UpdateFailed(
                f"Failed to aggregate Meraki data for org {self.org_id}: {e}"
            ) from e

        # Step 5: Update `self.data` with the fully processed and combined data.
        # This data becomes available to all entities listening to this
        # coordinator.
        self.data = combined_data
        # Obsolete comment about self.data["devices"] = devices removed.

        _LOGGER.debug(
            "Meraki data update completed for org %s. Processed: %d devices, %d SSIDs, %d networks.",
            self.org_id,
            len(devices),
            len(ssids),
            len(networks),
        )

        # Step 6: Handle tag erasing if the feature is enabled.
        # This iterates through the fetched devices and calls the tag eraser.
        if self.erase_tags and self.tag_eraser_coordinator:
            _LOGGER.warning(
                "Tag erasing is enabled for organization %s. Processing devices for tag removal.",
                self.org_id,
            )
            for (
                device_to_check
            ) in devices:  # Use a different variable name to avoid confusion
                serial = device_to_check.get("serial")
                if serial:
                    try:
                        await self.tag_eraser_coordinator.async_erase_device_tags(
                            serial
                        )
                    except (
                        MerakiApiError
                    ) as e:  # Handle errors during tag erasing for a single device.
                        _LOGGER.error(
                            "Failed to erase tags for device %s (org %s): %s",
                            serial,
                            self.org_id,
                            e,
                        )
        # Return the final, combined data.
        return self.data

    async def _async_shutdown(self) -> None:
        """Clean up resources when the coordinator is shut down.

        This method is called by Home Assistant when the integration or
        config entry is being unloaded. It should close any open connections,
        such as the Meraki API client session.
        """
        _LOGGER.debug(
            "MerakiDataUpdateCoordinator shutting down for org %s.", self.org_id
        )
        # Close the Meraki API client session.
        if hasattr(self, "meraki_client") and self.meraki_client:
            try:
                await self.meraki_client.close()
                _LOGGER.info(
                    "Meraki API client session closed for org %s.", self.org_id
                )
            except Exception as e:
                _LOGGER.error(
                    "Error closing Meraki API client session for org %s: %s",
                    self.org_id,
                    e,
                )

        # Call superclass shutdown for any base class cleanup.
        await super()._async_shutdown()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first data refresh for the config entry.

        This is called by Home Assistant after the config entry has been
        set up to perform an initial data fetch. It ensures that data is
        available before entities are created and added to Home Assistant.
        """
        _LOGGER.debug(
            "Performing first data refresh for Meraki config entry (org %s).",
            self.org_id,
        )
        await super().async_config_entry_first_refresh()
        _LOGGER.debug("First data refresh completed for org %s.", self.org_id)
