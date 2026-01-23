"""Sensor for Meraki switch port status."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiDevice


class MerakiSwitchPortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        assert self._device.serial
        self._port = port
        self._config_entry = config_entry

        self._attr_unique_id = f"{self._device.serial}_port_{self._port['portId']}"
        self._attr_name = f"{self._device.name} Port {self._port['portId']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(self.coordinator.DOMAIN, str(self._device.serial))},
        )

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                for port in self._device.ports_statuses:
                    if port["portId"] == self._port["portId"]:
                        self._port = port
                        break
                break
        self.async_write_ha_state()

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._port.get("status")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "enabled": self._port.get("enabled"),
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "port_id": self._port.get("portId"),
            "mac": self._device.mac,
        }
