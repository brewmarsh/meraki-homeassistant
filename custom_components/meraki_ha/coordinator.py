"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .coordinators.api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)
from .const import ERASE_TAGS_WARNING
from .coordinators.device_coordinator import MerakiDeviceCoordinator
from .coordinators.ssid_coordinator import MerakiSsidCoordinator
from .coordinators.network_coordinator import MerakiNetworkCoordinator
from .coordinators.device_tag_update_coordinator import DeviceTagUpdateCoordinator
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
        scan_interval: timedelta,
        device_name_format: str,
        erase_tags: bool,
        relaxed_tag_match: bool,
    ) -> None:
        """Initialize the Meraki data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.data = {}
        self.erase_tags = erase_tags
        self.relaxed_tag_match = relaxed_tag_match
        self.device_name_format = device_name_format
        self.hass = hass
        self.scan_interval = scan_interval
        self.device_tag_update_coordinator = DeviceTagUpdateCoordinator(
            self.hass, self.api_key, self.scan_interval
        )
        self.tag_eraser_coordinator = TagEraserCoordinator(
            self.hass, self.api_key, self.scan_interval
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        try:
            # Create coordinators within this method
            device_coordinator = MerakiDeviceCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            network_coordinator = MerakiNetworkCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            ssid_coordinator = MerakiSsidCoordinator(
                self.hass,
                self.api_key,
                self.org_id,
                self.scan_interval,
                self.device_name_format,
            )
            api_fetcher = MerakiApiDataFetcher(
                self.api_key, device_coordinator, network_coordinator, ssid_coordinator
            )
            device_tag_fetch_coordinator = DeviceTagFetchCoordinator(
                self.hass, self.api_key, self.scan_interval
            )
            data_aggregation_coordinator = DataAggregationCoordinator(
                self.hass, self.scan_interval, self.relaxed_tag_match
            )

            all_data = await api_fetcher.fetch_all_data(
                self.hass, self.org_id, self.scan_interval, self.device_name_format
            )

            devices: List[Dict[str, Any]] = all_data.get("devices", [])
            ssids: List[Dict[str, Any]] = all_data.get("ssids", [])
            networks: List[Dict[str, Any]] = all_data.get("networks", [])
            device_tags: Dict[str, List[str]] = {}
            for device in devices:
                serial = device["serial"]
                tags = await device_tag_fetch_coordinator.async_get_device_tags(serial)
                device_tags[serial] = tags
                device["tags"] = device_tags[serial]

            # **Explicitly update the coordinator data**
            device_coordinator.data = devices
            ssid_coordinator.data = ssids
            network_coordinator.data = networks

            combined_data = await data_aggregation_coordinator._async_update_data(
                device_coordinator.data,
                ssid_coordinator.data,
                network_coordinator.data,
                device_tags,
            )

            _LOGGER.debug(f"Meraki data update completed: {combined_data}")
            self.data = combined_data
            _LOGGER.debug(f"Coordinator data: {self.data}")

            if self.erase_tags:
                _LOGGER.warning(ERASE_TAGS_WARNING)
                for device in devices:
                    await self.tag_eraser_coordinator.async_erase_device_tags(
                        device["serial"]
                    )
            _LOGGER.debug(f"Coordinator data before return: {self.data}")

            return combined_data
        except MerakiApiConnectionError as e:
            _LOGGER.error(f"Connection error: {e}")
            raise UpdateFailed(f"Failed to connect to Meraki API: {e}")
        except MerakiApiInvalidApiKeyError as e:
            _LOGGER.error(f"Invalid API key: {e}")
            raise ConfigEntryAuthFailed(f"Invalid Meraki API key: {e}")
        except UpdateFailed as update_error:
            _LOGGER.error(f"Update failed: {update_error}")
            raise update_error
        except Exception as error:
            _LOGGER.exception(f"Unexpected error: {error}")
            raise UpdateFailed(f"Unexpected error: {error}")

    async def _async_shutdown(self):
        pass

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry."""
        try:
            await super().async_config_entry_first_refresh()
        finally:
            pass
