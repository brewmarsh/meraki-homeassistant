"""Sensor for tracking connected clients on a Meraki wireless device."""

from __future__ import annotations

import logging
from typing import Any

from ....core.entities.device import MerakiDeviceEntity
from ...coordinators import MerakiMainCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(MerakiDeviceEntity):
    """Representation of a Meraki Connected Clients Sensor."""

    _attr_icon = "mdi:wifi"
    _attr_native_unit_of_measurement = "clients"

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_serial: str,
    ) -> None:
        """
        Initialize the connected clients sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            device_serial: The serial number of the device.

        """
        super().__init__(
            coordinator=coordinator,
            device_serial=device_serial,
            name="Connected Clients",
            unique_id_suffix="connected_clients",
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of connected clients."""
        if not self.coordinator.data:
            return None

        clients_by_serial = self.coordinator.data.get("clients_by_serial", {})
        device_clients = clients_by_serial.get(self.device_serial)

        if device_clients is None:
            return 0

        return len(device_clients)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.device_data:
            return {}

        if isinstance(self.device_data, dict):
            return {
                "network_id": self.device_data.get("networkId"),
                "tags": self.device_data.get("tags", []),
            }

        return {
            "network_id": getattr(self.device_data, "network_id", None),
            "tags": getattr(self.device_data, "tags", []),
        }
