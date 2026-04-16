"""Connectivity binary sensor for Meraki hardware."""

from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.core import callback

from ...coordinators.base import MerakiBaseCoordinator
from ...core.models.device import MerakiDevice
from ...entity import MerakiBinarySensor

_LOGGER = logging.getLogger(__name__)

CONNECTIVITY_SENSOR_DESCRIPTION = BinarySensorEntityDescription(
    key="connectivity",
    name="Connectivity",
    device_class=BinarySensorDeviceClass.CONNECTIVITY,
)


class MerakiConnectivityBinarySensor(MerakiBinarySensor):
    """Representation of a Meraki hardware connectivity sensor."""

    entity_description = CONNECTIVITY_SENSOR_DESCRIPTION

    def __init__(
        self,
        coordinator: MerakiBaseCoordinator,
        device: MerakiDevice,
    ) -> None:
        """Initialize the connectivity sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{device.serial}_connectivity"
        self._attr_has_entity_name = True

    @property
    def is_on(self) -> bool:
        """Return true if the device is online."""
        device = self.device_data
        if not device:
            return False

        # We can use the model property if it's available
        if hasattr(device, "is_online"):
            return device.is_online

        # Fallback to manual check if it's a dict
        if isinstance(device, dict):
            status = device.get("status")
            return str(status).lower() in ("online", "alerting", "dormant")

        return False

    @property
    def available(self) -> bool:
        """Return if entity is available.

        A connectivity sensor is available as long as we have status data,
        even if the status itself is 'offline'.
        """
        if not self.coordinator.data:
            return False

        return self.device_data is not None

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return the state attributes."""
        device = self.device_data
        if not device:
            return {}

        if isinstance(device, dict):
            status = device.get("status")
            status_messages = device.get("statusMessages", [])
        else:
            status = getattr(device, "status", None)
            status_messages = getattr(device, "status_messages", [])

        return {
            "meraki_status": status,
            "status_messages": ", ".join(status_messages) if status_messages else None,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
