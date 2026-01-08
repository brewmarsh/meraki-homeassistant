"""Sensor for Meraki Device Serial Number."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSerialNumberSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Serial Number Sensor."""

    _attr_icon = "mdi:barcode"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_serial_number"
        self._attr_name = "Serial Number"
        self._attr_native_value = self._device_serial

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
        )

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
