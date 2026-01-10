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
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info
=======
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)

_LOGGER = logging.getLogger(__name__)


class MerakiMt20OpenCloseSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki MT20 open/close sensor."""

    _attr_device_class = BinarySensorDeviceClass.DOOR

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        device_info: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_info['serial']}-door"
        self._attr_name = f"{self._device_info['name']} Door"

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
                self.async_write_ha_state()
                return
        super()._handle_coordinator_update()

    @property
    def _door_reading(self) -> Any | None:
        """Get the 'door' reading value from the device data."""
        readings = self._device_info.get("readings")
        if not isinstance(readings, list):
            return None
        for reading in readings:
            if reading.get("metric") == "door":
                return reading.get("value")
        return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the door is open."""
        value = self._door_reading
        # The API returns a boolean for the 'door' metric, where True is open.
        return value if isinstance(value, bool) else None

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._door_reading is not None
