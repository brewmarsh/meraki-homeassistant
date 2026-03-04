"""Sensor for Meraki AP client count."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...entity import MerakiSensor
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiAPClientCountSensor(MerakiSensor):
    """Representation of a Meraki AP Client Count sensor."""

    _attr_icon = "mdi:account-network"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self.entity_description = SensorEntityDescription(
            key="ap_client_count",
            name="Client Count",
        )

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
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
        # Dynamic filtering of the coordinator's cached client list
        # as requested in the task requirements.
        clients = self.coordinator.data.get("clients") or []
        self._attr_native_value = sum(
            1
            for client in clients
            if isinstance(client, dict)
            and client.get("recentDeviceSerial") == self._device_serial
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
