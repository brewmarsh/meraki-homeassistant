"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .coordinators.api_data_fetcher import (
    MerakiApiDataFetcher,
)
from .const import ERASE_TAGS_WARNING
from .coordinators.ssid_coordinator import MerakiSsidCoordinator  # Corrected import
from .coordinators.network_coordinator import MerakiNetworkCoordinator
from .coordinators.tag_eraser_coordinator import TagEraserCoordinator
from .coordinators.data_aggregation_coordinator import DataAggregationCoordinator
from .coordinators.device_tag_fetch_coordinator import DeviceTagFetchCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        base_url: str,
        scan_interval: timedelta,
        # Pass instances of the sub-coordinators
        networks_coordinator: MerakiNetworkCoordinator,
        ssid_coordinator: MerakiSsidCoordinator,
        relaxed_tag_match: bool,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki data updater."""
        self.api_key = api_key
        self.org_id = org_id
        self.base_url = base_url
        self.networks_coordinator = networks_coordinator
        self.ssid_coordinator = ssid_coordinator
        self.config_entry = config_entry
        self.relaxed_tag_match = relaxed_tag_match
        self.erase_tags = config_entry.options.get(
            "erase_tags", False
        )  # Get 'erase_tags' option, default to False
        self.api_fetcher = MerakiApiDataFetcher(
            api_key, org_id, self.networks_coordinator, self.ssid_coordinator
        )
        # Initialize DeviceTagUpdateCoordinator here
        self.data_aggregation_coordinator = DataAggregationCoordinator(
            hass,
            scan_interval,
            relaxed_tag_match,
            self,  # Pass 'self' (the coordinator)
        )
        self.device_tag_fetch_coordinator = DeviceTagFetchCoordinator(
            hass, api_key, scan_interval, self
        )
        self.tag_eraser_coordinator = TagEraserCoordinator(
            hass, api_key, org_id, base_url
        )
        self.data: Dict[str, Any] = {}
        self.device_data: List[Dict[str, Any]] = []
        self.ssid_data: List[Dict[str, Any]] = []
        self.network_data: List[Dict[str, Any]] = []

        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        # **Use the existing coordinator instances to fetch data**
        all_data = await self.api_fetcher.fetch_all_data(
            self.hass,
            self.org_id,
            self.update_interval,
            self.config_entry.options.get("device_name_format", "prefix"),
        )

        devices: List[Dict[str, Any]] = all_data.get("devices", [])
        ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
        networks: List[Dict[str, Any]] = all_data.get("networks", [])
        device_tags: Dict[str, List[str]] = {}
        for device in devices:
            serial = device["serial"]
            tags = await self.device_tag_fetch_coordinator.async_get_device_tags(serial)
            device_tags[serial] = tags
            device["tags"] = device_tags[serial]

        # **Update the data within the existing coordinator instances**
        self.networks_coordinator.data = networks
        self.device_data = devices  # Store device data here if needed
        self.ssid_coordinator.data = ssids
        self.ssid_coordinator.networks = (
            self.networks_coordinator.data
        )  # Pass network data

        combined_data = await self.data_aggregation_coordinator._async_update_data(
            self.device_data,  # Use stored device data
            self.ssid_coordinator.data,
            self.networks_coordinator.data,
            device_tags,
        )

        # _LOGGER.debug(f"Meraki data update completed: {combined_data}")
        self.data = combined_data
        # **Explicitly include the devices list in self.data**
        self.data["devices"] = devices
        # _LOGGER.debug(f"Coordinator data: {self.data}")

        if self.erase_tags:
            _LOGGER.warning(ERASE_TAGS_WARNING)
            for device in devices:
                await self.tag_eraser_coordinator.async_erase_device_tags(
                    device["serial"]
                )
        # _LOGGER.debug(f"Coordinator data before return: {self.data}")

        return combined_data

    async def _async_shutdown(self):
        pass

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry."""
        await super().async_config_entry_first_refresh()
