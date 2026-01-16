"""Binary sensor for Meraki MT20 open/close sensor."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiMt20OpenCloseSensor(
    CoordinatorEntity,
    BinarySensorEntity,
    RestoreEntity,
):
    """Representation of a Meraki MT20 open/close sensor."""

    _attr_device_class = BinarySensorDeviceClass.DOOR

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_info['serial']}-door"
        self._attr_name = f"{self._device_info['name']} Door"
        self._attr_extra_state_attributes: dict[str, Any] = {}
        self._is_on: bool | None = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides unknown state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state == "on"
            if "ts" in last_state.attributes:
                self._attr_extra_state_attributes["ts"] = last_state.attributes["ts"]
            self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_info["serial"]:
                self._device_info = device
                readings = device.get("readings", [])
                if isinstance(readings, list):
                    for reading in readings:
                        if reading.get("metric") == "door":
                            door_data = reading.get("door", {})
                            if "open" in door_data:
                                self._is_on = door_data["open"]
                            if "ts" in reading:
                                self._attr_extra_state_attributes["ts"] = reading["ts"]
                self.async_write_ha_state()
                return
        super()._handle_coordinator_update()

    @property
    def is_on(self) -> bool | None:
        """Return true if the door is open."""
        return self._is_on

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._device_info is not None
