"""Sensor for tracking connected clients on a Meraki wireless device."""
from __future__ import annotations

import logging
from typing import Any

from ....coordinator import MerakiDataUpdateCoordinator
from ....core.entities.device import MerakiDeviceEntity

_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(MerakiDeviceEntity):

    """Representation of a Meraki Connected Clients Sensor."""

    _attr_icon = "mdi:wifi"
    _attr_native_unit_of_measurement = "clients"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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
        return self.device_data.get("clients") if self.device_data else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.device_data:
            return {}
        return {
            "network_id": self.device_data.get("networkId"),
            "tags": self.device_data.get("tags", []),
        }
