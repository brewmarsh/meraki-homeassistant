"""Text entity for controlling Meraki SSID Name."""

import logging
from typing import Any

from homeassistant.components.text import TextEntity, TextEntityDescription, TextMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..core.api.client import MerakiAPIClient
from ..helpers.device_info_helpers import resolve_device_info
from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDNameText(CoordinatorEntity, TextEntity):
    """Representation of a Meraki SSID Name text entity."""

    _attr_mode = TextMode.TEXT  # Or TextMode.PASSWORD if it were a password
    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,  # Added to match switch entities
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID Name text entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry  # Store config_entry
        self._ssid_data = ssid_data

        # These are crucial for API calls to update the SSID name
        self._network_id: str | None = ssid_data.get("networkId")
        self._ssid_number: Any | None = ssid_data.get(
            "number"
        )  # Can be int or str depending on source

        # EntityDescription can be used for name, icon etc.
        self.entity_description = TextEntityDescription(
            key=f"ssid-{self._network_id}-{self._ssid_number}_ssid_name",
            name="SSID Name",
            icon="mdi:form-textbox",
            native_min=1,
            native_max=32,
        )

        self._attr_unique_id = f"ssid-{self._network_id}-{self._ssid_number}_name_text"

        # Set initial state
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the SSID device."""
        return resolve_device_info(
            entity_data={"networkId": self._network_id},
            config_entry=self._config_entry,
            ssid_data=self._ssid_data,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        # This entity should be available as long as we have data for the SSID,
        # regardless of whether the SSID is enabled or not.
        return ssid_data is not None

    def _get_current_ssid_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return None
        for ssid in self.coordinator.data["ssids"]:
            if ssid.get("networkId") == self._network_id and str(
                ssid.get("number")
            ) == str(self._ssid_number):
                return ssid
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the text entity based on coordinator data."""
        # Ignore coordinator data to avoid overwriting optimistic state
        if self.coordinator.is_update_pending(self.unique_id):
            return

        current_ssid_data = self._get_current_ssid_data()
        if current_ssid_data:
            self._attr_native_value = current_ssid_data.get("name")
        else:
            self._attr_native_value = None

    async def async_set_value(self, value: str) -> None:
        """Change the SSID name."""
        if self._network_id is None or self._ssid_number is None:
            _LOGGER.error(
                "Cannot update SSID name for %s: Missing networkId or SSID number.",
                self.entity_id or self._attr_unique_id,
            )
            return

        # Optimistically update the state so the UI responds immediately.
        self._attr_native_value = value
        self.async_write_ha_state()

        try:
            await self._meraki_client.wireless.update_network_wireless_ssid(
                network_id=self._network_id,
                number=str(self._ssid_number),
                name=value,
            )
            # Register a pending update to prevent overwriting the optimistic state
            self.coordinator.register_pending_update(self.unique_id)
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set SSID name for network %s, SSID %s to '%s': %s",
                self._network_id,
                self._ssid_number,
                value,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set SSID name to '{value}': {e}"
            ) from e
