"""Sensor for Meraki Switch client count."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinators import MerakiSwitchCoordinator
from ...entity import MerakiSensor

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchClientCountSensor(MerakiSensor):
    """Representation of a Meraki Switch Client Count sensor."""

    _attr_icon = "mdi:account-network"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self.entity_description = SensorEntityDescription(
            key="switch_client_count",
            name="Client Count",
        )

        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self._device_serial:
            return self.coordinator.get_device(self._device_serial)
        return None

    @callback
    def _update_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        if not self.coordinator.data:
            self._attr_native_value = 0
            return

        clients_by_serial = self.coordinator.data.get("clients_by_serial", {})
        device_clients = clients_by_serial.get(self._device_serial)

        if device_clients is None:
            self._attr_native_value = 0
            return

        self._attr_native_value = len(device_clients)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.coordinator.data is None:
            return False
        return super().available and self._get_current_device_data() is not None
