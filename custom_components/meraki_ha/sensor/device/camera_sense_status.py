"""Sensor entity for Meraki camera sense status."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseStatusSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki Camera Sense Status sensor."""

    coordinator: MerakiDataCoordinator
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Mapping[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Camera Sense Status sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_camera_sense_status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
        )
        self.entity_description = SensorEntityDescription(
            key="camera_sense_status",
            name="Sense Enabled",
            native_unit_of_measurement=None,
            state_class=None,
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = "unavailable"
            self._attr_icon = "mdi:help-rhombus"
            self._attr_extra_state_attributes = {
                "serial_number": self._device_serial,
            }
            return

        # sense_settings contains the senseEnabled field from the API
        sense_settings = current_device_data.get("sense_settings", {})
        sense_enabled_value = (
            sense_settings.get("senseEnabled")
            if isinstance(sense_settings, dict)
            else None
        )

        if sense_enabled_value is None:
            # Sense not configured/licensed for this camera
            self._attr_native_value = "not_configured"
            self._attr_icon = "mdi:camera-off-outline"
        else:
            sense_enabled = bool(sense_enabled_value)
            self._attr_native_value = "enabled" if sense_enabled else "disabled"
            self._attr_icon = (
                "mdi:camera-iris" if sense_enabled else "mdi:camera-off-outline"
            )

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
        }
        if self.coordinator.last_successful_update:
            self._attr_extra_state_attributes["last_meraki_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available (device exists in coordinator)."""
        if not super().available:
            return False

        # Available as long as the device exists in coordinator data
        current_device_data = self._get_current_device_data()
        return current_device_data is not None
