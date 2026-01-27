"""Sensor entity for Meraki camera sense status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Camera Sense Status sensor."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Camera Sense Status sensor."""
        super().__init__(coordinator)
        assert device_data.serial is not None
        self._device_serial: str = device_data.serial
        self._attr_unique_id = f"{self._device_serial}_camera_sense_status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.model,
            manufacturer="Cisco Meraki",
        )
        self.entity_description = SensorEntityDescription(
            key="camera_sense_status",
            name="Sense Enabled",
            native_unit_of_measurement=None,
            state_class=None,
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        sense_settings = getattr(current_device_data, "sense_settings", None)

        if not isinstance(sense_settings, dict):
            self._attr_native_value = None
            self._attr_icon = "mdi:camera-question"
            return

        sense_enabled_value = sense_settings.get("senseEnabled")

        if sense_enabled_value is None:
            self._attr_native_value = None
            self._attr_icon = "mdi:camera-question"
        else:
            sense_enabled = bool(sense_enabled_value)
            self._attr_native_value = "enabled" if sense_enabled else "disabled"
            self._attr_icon = (
                "mdi:camera-iris" if sense_enabled else "mdi:camera-off-outline"
            )

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available:
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False

        sense_settings = getattr(current_device_data, "sense_settings", None)
        return isinstance(sense_settings, dict)
