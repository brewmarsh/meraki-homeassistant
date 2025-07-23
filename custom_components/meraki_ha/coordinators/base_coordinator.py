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

from ..const import DOMAIN, ERASE_TAGS_WARNING  # Changed to relative import
from ..api.meraki_api import MerakiApiError
from .api_data_fetcher import MerakiApiDataFetcher
from .data_aggregation_coordinator import DataAggregationCoordinator

# Added imports for device registration
from homeassistant.helpers import device_registry as dr
from .helpers.naming_utils import format_device_name


# Obsolete coordinators (DeviceTagFetchCoordinator,
# MerakiNetworkCoordinator, MerakiSsidCoordinator) removed.
from .tag_eraser_coordinator import (
    TagEraserCoordinator,
)

import asyncio  # Make sure asyncio is imported

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
        config_entry: ConfigEntry,  # relaxed_tag_match parameter removed
    ) -> None:
        """Initialize the Meraki data update coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key, used for initializing MerakiAPIClient and potentially TagEraserCoordinator.
            org_id: The Meraki Organization ID.
            scan_interval: The interval at which to periodically update data.
            config_entry: The config entry associated with this coordinator instance,
                          used for accessing options (e.g., erase_tags, device_name_format)
                          and for device registration.
        """
        self.api_key: str = api_key  # Stored for potential direct use (e.g., TagEraser)
        self.org_id: str = org_id
        self.config_entry: ConfigEntry = config_entry  # Access to options, entry_id
        # self.relaxed_tag_match attribute removed
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        # Initialize the MerakiAPIClient for SDK interactions.
        # This client is passed to the api_fetcher and its lifecycle managed
        # here.
        # Local import to avoid potential circulars
        from ..api.meraki_api import MerakiAPIClient

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
                # relaxed_tag_match argument removed
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
        self.org_name: Optional[str] = None  # Initialize org_name
        self.formatted_org_display_name: Optional[str] = None
        self._is_available = True

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
        try:
            await self.meraki_client.initialize()
            all_data: Dict[str, Any] = await self.api_fetcher.fetch_all_data(
                self.hass,
            )
        except (
            MerakiApiError,
            asyncio.TimeoutError,
        ) as e:  # Handle both API and timeout errors
            if self._is_available:
                _LOGGER.error(
                    "API/Network error during Meraki data fetch for org %s: %s. Type: %s",
                    self.org_id,
                    str(e),
                    type(e).__name__,
                )
                self._is_available = False
            raise UpdateFailed(
                f"Failed to fetch data from Meraki API for org {self.org_id}: {e}"
            ) from e
        except (
            Exception
        ) as e:  # Catch any other unexpected errors during the main fetch
            if self._is_available:
                _LOGGER.exception(
                    "Unexpected error during Meraki data fetch for org %s: %s. Error type: %s",
                    self.org_id,
                    str(e),
                    type(e).__name__,
                )
                self._is_available = False
            raise UpdateFailed(
                f"Unexpected error fetching data for org {self.org_id}: {e}"
            ) from e
        if not all_data:
            raise UpdateFailed("No data received from Meraki API")

        # Extract data components from `all_data`. Default to empty lists if
        # keys are missing.
        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])
        clients_list: List[Dict[str, Any]] = all_data.get(
            "clients", []
        )  # New: Extract clients
        self.org_name = all_data.get("org_name")  # Store org_name from fetched data

        # Step 2: Device tags are now part of the `devices` list from `all_data`.
        # No separate tag fetching step is needed here.

        # Step 3: Obsolete step for updating separate network/SSID coordinators removed.
        # Data is passed directly to the DataAggregationCoordinator.

        # Store the fetched devices list internally. This list includes tags
        # and MR-specific details.
        self.device_data = devices

        # ---- START NETWORK DEVICE REGISTRATION LOGIC ----
        device_registry = dr.async_get(self.hass)
        processed_network_devices = 0
        for network_info in networks:
            network_id = network_info.get("id")
            network_name = network_info.get("name")

            if not network_id:
                _LOGGER.warning(
                    "Found a network with missing ID, cannot register as HA device: %s",
                    network_info,
                )
                continue
            if not network_name:
                original_network_name = f"Meraki Network {network_id}"
                _LOGGER.warning(
                    "Found network with missing name (ID: %s), using fallback name: %s",
                    network_id,
                    original_network_name,
                )
            else:
                original_network_name = network_name

            current_device_name_format = self.device_name_format
            formatted_network_name = format_device_name(
                device_name_raw=original_network_name,
                device_model="Network",
                device_name_format_option=current_device_name_format,
                is_org_device=False,
            )
            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, network_id)},
                name=formatted_network_name,
                model=f"Network (ID: {network_id})",
                manufacturer="Cisco Meraki",
            )
            processed_network_devices += 1

        for device_info in devices:
            serial = device_info.get("serial")
            if not serial:
                _LOGGER.warning(
                    "Device found without serial, cannot register: %s", device_info
                )
                continue

            device_name_raw = device_info.get("name") or serial
            device_model_str = device_info.get("model", "Unknown")
            firmware_version = device_info.get("firmware")

            formatted_device_name = format_device_name(
                device_name_raw=device_name_raw,
                device_model=device_model_str,
                device_name_format_option=self.device_name_format,
                is_org_device=False,
            )

            mac_address = device_info.get("mac")
            connections = None
            if mac_address:
                connections = {(dr.CONNECTION_NETWORK_MAC, mac_address)}

            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, serial)},
                manufacturer="Cisco Meraki",
                model=device_model_str,
                name=formatted_device_name,
                sw_version=firmware_version,
                connections=connections,
            )
        from .data_processor import (
            MerakiDataProcessor,
        )  # Ensure import

        processor = MerakiDataProcessor(self)  # Instantiate processor
        network_client_counts = processor.process_network_client_counts(clients_list)

        # Extract the new organization-wide client counts from all_data
        clients_on_ssids = all_data.get("clients_on_ssids", 0)
        clients_on_appliances = all_data.get("clients_on_appliances", 0)
        clients_on_wireless = all_data.get("clients_on_wireless", 0)

        if not self._is_available:
            _LOGGER.info("Connection to Meraki API restored for org %s", self.org_id)
            self._is_available = True

        # Step 4: Aggregate all data using the DataAggregationCoordinator.
        # This coordinator takes the raw lists of devices, SSIDs, and networks.
        try:
            combined_data: Dict[str, Any] = (
                await self.data_aggregation_coordinator._async_update_data(
                    devices,
                    ssids,
                    networks,
                    clients_list,
                    network_client_counts,
                    clients_on_ssids=clients_on_ssids,
                    clients_on_appliances=clients_on_appliances,
                    clients_on_wireless=clients_on_wireless,
                )
            )
        except (
            KeyError,
            ValueError,
            TypeError,
        ) as e:  # Handle data structure/type errors
            error_msg = f"Data structure error during aggregation for org {self.org_id}: {str(e)}"
            _LOGGER.error("%s. Error type: %s", error_msg, type(e).__name__)
            raise UpdateFailed(error_msg) from e
        except Exception as e:  # Catch any other unexpected errors
            error_msg = f"Unexpected error during data aggregation for org {self.org_id}: {str(e)}"
            _LOGGER.exception("%s. Error type: %s", error_msg, type(e).__name__)
            raise UpdateFailed(error_msg) from e

        self.data = combined_data

        if self.erase_tags and self.tag_eraser_coordinator:
            _LOGGER.warning(
                "Tag erasing is enabled for organization %s. Processing devices for tag removal.",
                self.org_id,
            )
            for device_to_check in devices:
                serial = device_to_check.get("serial")
                if serial:
                    try:
                        await self.tag_eraser_coordinator.async_erase_device_tags(
                            serial
                        )
                    except MerakiApiError as e:
                        _LOGGER.error(
                            "Failed to erase tags for device %s (org %s): %s. Error type: %s",
                            serial,
                            self.org_id,
                            str(e),
                            type(e).__name__,
                        )
                    except asyncio.TimeoutError:
                        _LOGGER.error(
                            "Network timeout while erasing tags for device %s (org %s)",
                            serial,
                            self.org_id,
                        )
                    except Exception as e:
                        _LOGGER.exception(
                            "Unexpected error erasing tags for device %s (org %s): %s",
                            serial,
                            self.org_id,
                            str(e),
                        )
        await self._device_registry_cleanup()
        return self.data

    async def async_register_organization_device(self, hass: HomeAssistant) -> None:
        """Register the Meraki Organization as a device in Home Assistant."""
        if not self.org_id:
            _LOGGER.error(
                "Organization ID not available, cannot register organization device."
            )
            return

        raw_org_name = (
            self.org_name if self.org_name else f"Meraki Organization {self.org_id}"
        )
        device_name_format_option = self.device_name_format

        # _LOGGER.debug(
        #     "OrgDevReg: Raw org name: '%s', Name format option: '%s'",
        #     raw_org_name,
        #     device_name_format_option
        # ) # Reduced verbosity

        formatted_org_name = format_device_name(
            device_name_raw=raw_org_name,
            device_model="Organization",
            device_name_format_option=device_name_format_option,
            is_org_device=True,
        )
        # _LOGGER.debug("OrgDevReg: Formatted org name: '%s'", formatted_org_name) # Reduced verbosity
        self.formatted_org_display_name = formatted_org_name

        device_registry = dr.async_get(hass)
        device_registry.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, self.org_id)},
            name=formatted_org_name,
            model="Organization",
            manufacturer="Cisco Meraki",
        )
        # _LOGGER.debug(
        #     "Organization device registration attempt complete for %s.", self.org_id
        # ) # Corrected: Removed stray parenthesis here

    async def _device_registry_cleanup(self) -> None:
        """Remove stale devices from the device registry."""
        device_registry = dr.async_get(self.hass)
        current_devices = {
            (DOMAIN, device["serial"])
            for device in self.data.get("devices", [])
            if "serial" in device
        }
        for device in dr.async_entries_for_config_entry(
            device_registry, self.config_entry.entry_id
        ):
            if not any(
                identifier in current_devices for identifier in device.identifiers
            ):
                device_registry.async_remove_device(device.id)

    async def _async_shutdown(self) -> None:
        """Clean up resources when the coordinator is shut down.

        This method is called by Home Assistant when the integration or
        config entry is being unloaded. It should close any open connections,
        such as the Meraki API client session.
        """
        # Close the Meraki API client session.
        if hasattr(self, "meraki_client") and self.meraki_client:
            try:
                await self.meraki_client.close()
            except (asyncio.TimeoutError, ConnectionError) as e:
                _LOGGER.warning(
                    "Network error while closing Meraki API client session for org %s: %s",
                    self.org_id,
                    str(e),
                )
            except Exception as e:
                _LOGGER.error(
                    "Unexpected error closing Meraki API client session for org %s: %s. Error type: %s",
                    self.org_id,
                    str(e),
                    type(e).__name__,
                )

        # Call superclass shutdown for any base class cleanup.
        await super()._async_shutdown()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first data refresh for the config entry.

        This is called by Home Assistant after the config entry has been
        set up to perform an initial data fetch. It ensures that data is
        available before entities are created and added to Home Assistant.
        """
        await super().async_config_entry_first_refresh()
