"""Select entity for controlling Meraki Network Content Filtering."""

import logging
from typing import Any, Dict

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..core.coordinators.network_content_filtering_coordinator import (
    NetworkContentFilteringCoordinator,
)
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkContentFilteringSelect(
    CoordinatorEntity[NetworkContentFilteringCoordinator], SelectEntity
):
    """Representation of a Meraki Network Content Filtering select entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NetworkContentFilteringCoordinator,
        config_entry: ConfigEntry,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Network Content Filtering select entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data["id"]

        self.entity_description = SelectEntityDescription(
            key=f"network_content_filtering_{self._network_id}",
            name="Content Filtering Policy",
            icon="mdi:web-filter",
        )

        self._attr_unique_id = (
            f"meraki-network-{self._network_id}-content-filtering"
        )
        self._attr_options = ["high", "moderate", "low", "approved"]  # Static for now
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
        if self.coordinator.data:
            self._attr_current_option = self.coordinator.data.get("settings")
        else:
            self._attr_current_option = None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            await self.coordinator.async_update_content_filtering(settings=option)
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
