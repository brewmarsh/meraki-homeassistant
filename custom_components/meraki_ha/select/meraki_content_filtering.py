"""Select entity for controlling Meraki SSID Content Filtering."""

import logging
from typing import Any, Dict

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..core.coordinators.ssid_content_filtering_coordinator import (
    SsidContentFilteringCoordinator,
)
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSsidContentFilteringSelect(
    CoordinatorEntity[SsidContentFilteringCoordinator], SelectEntity
):
    """Representation of a Meraki SSID Content Filtering select entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SsidContentFilteringCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID Content Filtering select entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_data = ssid_data
        self._network_id = ssid_data["networkId"]
        self._ssid_number = ssid_data["number"]

        self.entity_description = SelectEntityDescription(
            key=f"content_filtering_{self._network_id}_{self._ssid_number}",
            name="Content Filtering Policy",
            icon="mdi:web-filter",
        )

        self._attr_unique_id = (
            f"meraki-ssid-{self._network_id}-{self._ssid_number}-content-filtering"
        )
        self._attr_options = ["high", "moderate", "low", "approved"]  # Static for now
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the SSID device."""
        return resolve_device_info(
            entity_data=self._ssid_data,
            config_entry=self._config_entry,
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data:
            return {
                "blocked_categories": self.coordinator.data.get(
                    "blocked_categories_names", []
                )
            }
        return {}

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
        if self.coordinator.data and "contentFiltering" in self.coordinator.data:
            self._attr_current_option = self.coordinator.data["contentFiltering"].get(
                "settings"
            )
        else:
            self._attr_current_option = None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            await self.coordinator.async_update_content_filtering(settings=option)
        except Exception as e:
            _LOGGER.error(
                "Failed to set content filtering policy to '%s' for SSID %s: %s",
                option,
                self._ssid_number,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set content filtering policy to '{option}': {e}"
            ) from e
