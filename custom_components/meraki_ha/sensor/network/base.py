"""Base class for Meraki SSID sensors."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Meraki SSID sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        attribute: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_data_at_init = ssid_data
        self._attribute = attribute
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._attr_unique_id = (
            f"ssid-{self._network_id}-{self._ssid_number}-{self._attribute}"
        )
        # Set device_info directly in init
        self._attr_device_info = resolve_device_info(
            entity_data=self._ssid_data_at_init,
            config_entry=self._config_entry,
        )

    def _get_current_ssid_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this SSID from the coordinator."""
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return None
        for ssid in self.coordinator.data["ssids"]:
            if ssid.get("networkId") == self._network_id and str(
                ssid.get("number")
            ) == str(self._ssid_number):
                return ssid
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        return ssid_data is not None and ssid_data.get("enabled", False)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        ssid_data = self._get_current_ssid_data()
        if ssid_data:
            self._attr_native_value = ssid_data.get(self._attribute)
        self.async_write_ha_state()
