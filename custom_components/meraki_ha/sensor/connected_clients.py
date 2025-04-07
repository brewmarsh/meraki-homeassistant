"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback


_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Connected Clients sensor."""

    def __init__(self, coordinator: CoordinatorEntity, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Connected Clients sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")
        self._attr_name = f"{device['name']} Connected Clients"
        self._attr_unique_id = f"{device['serial']}_connected_clients"
        self._attr_icon = "mdi:account-network"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        _LOGGER.debug(
            f"Meraki: Connected Clients Sensor Initialized: {self._attr_name}"
        )
        self._attr_native_value = self._get_client_count()
        self._attr_native_unit_of_measurement = "clients"
        self._attr_state_class = "measurement"

    def _get_client_count(self) -> Optional[int]:
        """Get the client count from the coordinator data."""
        _LOGGER.debug(f"Meraki: Getting client count for {self._device['serial']}")
        _LOGGER.debug(f"Meraki: Coordinator data: {self.coordinator.data}")
        device_data = next(
            (
                d
                for d in self.coordinator.data.get("devices", [])
                if d["serial"] == self._device["serial"]
            ),
            None,
        )
        if device_data:
            _LOGGER.debug(f"Meraki: Found device data: {device_data}")
            _LOGGER.debug(
                f"Meraki: Connected clients data: {device_data.get('connected_clients')}"
            )
            connected_clients = device_data.get("connected_clients")
            if connected_clients is not None:
                _LOGGER.debug(f"Meraki: Connected clients: {connected_clients}")
                return connected_clients
            else:
                _LOGGER.warning(
                    f"Meraki: 'connected_clients' value is None for {self._device['serial']}"
                )
                return 0
        else:
            _LOGGER.warning(
                f"Meraki: Device data not found for {self._device['serial']}"
            )
            return 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._get_client_count()
        self.async_write_ha_state()

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()
