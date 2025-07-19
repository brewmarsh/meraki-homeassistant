"""Sensor for tracking connected clients on a Meraki wireless device."""

import logging
from typing import Any, Dict

from ....entities import MerakiDeviceEntity

_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(MerakiDeviceEntity):
    """Representation of a Meraki Connected Clients Sensor."""

    _attr_icon = "mdi:wifi"
    _attr_native_unit_of_measurement = "clients"

    def __init__(
        self,
        coordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the connected clients sensor."""
        super().__init__(
            coordinator=coordinator,
            device_data=device_data,
            name="Connected Clients",
            unique_id_suffix="connected_clients",
        )
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_data = self._get_device_data()

        if not current_device_data:
            self._attr_native_value = 0
            self._attr_extra_state_attributes = {}
            return

        # Get connected clients count, defaulting to 0 if not available
        clients_count = current_device_data.get("connected_clients_count")
        if not isinstance(clients_count, int):
            _LOGGER.warning(
                "Connected clients data for device '%s' (Serial: %s) is not an integer: %s. Defaulting to 0.",
                current_device_data.get("name", "Unknown"),
                self._device_serial,
                clients_count,
            )
            clients_count = 0

        self._attr_native_value = clients_count

        # Update attributes with any client-related data
        self._attr_extra_state_attributes = {
            "network_id": current_device_data.get("networkId"),
            "tags": current_device_data.get("tags", []),
        }
