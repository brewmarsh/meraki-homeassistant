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

from ..core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)

# These are the options provided by the Meraki API
FILTERING_OPTIONS = {
    "Strict": {"id": "strict", "name": "Strict"},
    "Normal": {"id": "normal", "name": "Normal"},
    "Top Sites": {"id": "topSites", "name": "Top Sites"},
    "Whitelist": {"id": "whitelist", "name": "Whitelist"},
    "Disabled": {"id": "disabled", "name": "Disabled"},
}


class MerakiContentFilteringSelect(
    CoordinatorEntity[SsidFirewallCoordinator], SelectEntity
):
    """Representation of a Meraki Content Filtering select entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        firewall_coordinator: SsidFirewallCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Content Filtering select entity."""
        super().__init__(firewall_coordinator)
        self._config_entry = config_entry
        self._ssid_data = ssid_data
        self._ssid_number = ssid_data["number"]

        self.entity_description = SelectEntityDescription(
            key=f"content_filtering_{self._ssid_number}",
            name="Content Filtering",
            icon="mdi:web-filter",
            options=[option["name"] for option in FILTERING_OPTIONS.values()],
        )

        self._attr_unique_id = (
            f"meraki-ssid-{self._ssid_number}-content-filtering"
        )
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the SSID device."""
        return resolve_device_info(
            entity_data=self._ssid_data,
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
        if not self.coordinator.data:
            self._attr_current_option = None
            return

        settings = self.coordinator.data.get("settings", {})
        policy = settings.get("blockedUrlCategories", [])

        if not settings.get("enabled", False) or not policy:
            self._attr_current_option = FILTERING_OPTIONS["Disabled"]["name"]
        elif "Top Sites" in policy:
            self._attr_current_option = FILTERING_OPTIONS["Top Sites"]["name"]
        elif "Strict" in policy:
            self._attr_current_option = FILTERING_OPTIONS["Strict"]["name"]
        elif "Normal" in policy:
            self._attr_current_option = FILTERING_OPTIONS["Normal"]["name"]
        else:
            self._attr_current_option = FILTERING_OPTIONS["Whitelist"]["name"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        api_option_id = next(
            (
                opt["id"]
                for opt in FILTERING_OPTIONS.values()
                if opt["name"] == option
            ),
            None,
        )
        if api_option_id is None:
            raise HomeAssistantError(f"Invalid content filtering option: {option}")

        try:
            await self.coordinator.async_update_content_filtering(api_option_id)
            self._attr_current_option = option
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(
                "Failed to set content filtering to '%s' for SSID %s: %s",
                option,
                self._ssid_number,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set content filtering to '{option}': {e}"
            ) from e
