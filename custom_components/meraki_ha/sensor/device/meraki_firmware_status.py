from __future__ import annotations

"""Sensor for Meraki Device Firmware Status."""

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
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


class MerakiFirmwareStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Firmware Status Sensor."""

    _attr_icon = "mdi:package-up"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["up_to_date", "update_available", "unknown"]

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data.serial
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_firmware_status"
        self._attr_name = "Firmware Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.model,
            manufacturer="Cisco Meraki",
            sw_version=device_data.firmware,
        )

        self._attr_extra_state_attributes: dict[str, Any] = {}
        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = "unknown"
            self._attr_extra_state_attributes = {}
            return

        firmware_upgrades = current_device_data.firmware_upgrades or {}
        if firmware_upgrades.get("available"):
            self._attr_native_value = "update_available"
        else:
            self._attr_native_value = "up_to_date"

        attributes = {
            "current_firmware_version": current_device_data.firmware,
            "latest_available_firmware_version": firmware_upgrades.get(
                "latestVersion", {}
            ).get("shortName"),
            "next_upgrade_version": firmware_upgrades.get("nextUpgrade", {})
            .get("toVersion", {})
            .get("shortName"),
            "next_upgrade_time": firmware_upgrades.get("nextUpgrade", {}).get("time"),
            "model": current_device_data.model,
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
