"""Sensor for Meraki Device Firmware Status."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiFirmwareStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Firmware Status Sensor."""

    _attr_icon = "mdi:package-up"
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["up_to_date", "update_available", "unknown"]

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Mapping[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_firmware_status"
        self._attr_name = "Firmware Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            sw_version=device_data.get("firmware"),
        )

        self._attr_extra_state_attributes: dict[str, Any] = {}
        self._update_state()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = "unknown"
            self._attr_extra_state_attributes = {}
            return

        firmware_upgrades = current_device_data.get("firmware_upgrades")
        if firmware_upgrades and firmware_upgrades.get("available"):
            self._attr_native_value = "update_available"
        else:
            self._attr_native_value = "up_to_date"

        attributes = {
            "current_firmware_version": current_device_data.get("firmware"),
            "latest_available_firmware_version": firmware_upgrades.get(
                "latestVersion", {}
            ).get("shortName")
            if firmware_upgrades
            else None,
            "next_upgrade_version": firmware_upgrades.get("nextUpgrade", {})
            .get("toVersion", {})
            .get("shortName")
            if firmware_upgrades
            else None,
            "next_upgrade_time": firmware_upgrades.get("nextUpgrade", {}).get("time")
            if firmware_upgrades
            else None,
            "model": current_device_data.get("model"),
        }

        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
