"""Select entity for controlling Meraki Content Filtering."""

import logging
from typing import Any, Dict

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiContentFilteringSelect(
    CoordinatorEntity[MerakiDataCoordinator], SelectEntity
):
    """Representation of a Meraki Content Filtering select entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Content Filtering select entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data["id"]

        self.entity_description = SelectEntityDescription(
            key=f"content_filtering_{self._network_id}",
            name="Content Filtering Policy",
            icon="mdi:web-filter",
        )

        self._attr_unique_id = f"meraki-network-{self._network_id}-content-filtering"
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the network device."""
        return resolve_device_info(
            entity_data=self._network_data,
            config_entry=self._config_entry,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the select entity."""
        if self.coordinator.data and self.coordinator.data.get("content_filtering"):
            content_filtering = self.coordinator.data["content_filtering"].get(
                self._network_id
            )
            if content_filtering:
                self._attr_current_option = content_filtering.get(
                    "urlCategoryListSize", "topSites"
                )
                self._attr_options = [
                    "topSites",
                    "fullList",
                ]  # This should be dynamic
        else:
            self._attr_current_option = None
            self._attr_options = []

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            await self._meraki_client.appliance.update_network_appliance_content_filtering(
                networkId=self._network_id,
                urlCategoryListSize=option,
            )
            self._attr_current_option = option
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set content filtering policy to '%s' for network %s: %s",
                option,
                self._network_id,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set content filtering policy to '{option}': {e}"
            ) from e
