"""Bandwidth sensors for Meraki appliance uplinks."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfDataRate

from ...entity import MerakiSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from ...coordinators import MerakiApplianceCoordinator
    from ...core.models.device import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MerakiBandwidthSensor(MerakiSensor, SensorEntity):
    """Representation of an appliance uplink bandwidth sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.DATA_RATE
    _attr_native_unit_of_measurement = UnitOfDataRate.MEGABITS_PER_SECOND
    _attr_entity_registry_enabled_default = False  # Opt-in by default

    def __init__(
        self,
        coordinator: MerakiApplianceCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        direction: str,  # "sent" or "received"
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the bandwidth sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_serial = device.serial
        self._config_entry = config_entry
        self._interface = interface
        self._direction = direction
        self.entity_description = description
        self._attr_unique_id = f"{device.serial}_bandwidth_{interface}_{direction}"

    @property
    def native_value(self) -> float | None:
        """Return the bandwidth value in Mb/s."""
        device_data = self.device_data
        if not device_data:
            return None

        # Bandwidth data can be in uplink_usage_history or unified uplinks
        usage_history = getattr(device_data, "uplink_usage_history", [])
        if not usage_history:
            usage_history = getattr(device_data, "uplinks", [])

        if not isinstance(usage_history, list):
            return None

        for entry in usage_history:
            if entry.get("interface") == self._interface:
                value = entry.get(self._direction)
                if value is None:
                    # Fallback for "received" vs "recv" if necessary
                    if self._direction == "received":
                        value = entry.get("recv")

                if value is None:
                    return None

                # Meraki returns bytes, we want Megabits per second
                # Assuming the history interval is 60s (default)
                # (Bytes * 8) / (1024 * 1024) / 60
                megabits = (value * 8) / (1024 * 1024)
                return round(megabits / 60, 2)

        return None
