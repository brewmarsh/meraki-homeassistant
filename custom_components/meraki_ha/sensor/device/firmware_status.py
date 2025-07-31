"""Sensor for Meraki device firmware status."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Meraki firmware status sensors from a config entry."""
    device_coordinator = hass.data[DOMAIN][config_entry.entry_id]["device_coordinator"]
    entities = []
    for device in device_coordinator.data.get("devices", []):
        entities.append(MerakiFirmwareStatusSensor(device_coordinator, device))
    async_add_entities(entities, True)


class MerakiFirmwareStatusSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki device firmware status sensor."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_firmware_status"
        self._attr_name = f"{self._device['name']} Firmware Status"
        self._attr_icon = "mdi:package-up"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self._device.get("firmware_upgrades", {}).get("available"):
            return "update_available"
        return "up_to_date"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "current_version": self._device.get("firmware"),
            "latest_version": self._device.get("firmware_upgrades", {}).get(
                "latestVersion", {}
            ).get("shortName"),
            "next_upgrade_version": self._device.get("firmware_upgrades", {}).get(
                "nextUpgrade", {}
            ).get("toVersion", {}).get("shortName"),
            "next_upgrade_time": self._device.get("firmware_upgrades", {}).get(
                "nextUpgrade", {}
            ).get("time"),
        }
