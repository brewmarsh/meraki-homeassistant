"""Binary sensor for Meraki appliance port status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.models import MerakiAppliancePort
from ...core.models.device import MerakiDevice
from ...entity import MerakiBinarySensor

if TYPE_CHECKING:
    from ...coordinators import MerakiApplianceCoordinator


class AppliancePortBinarySensor(MerakiBinarySensor):
    """Representation of a Meraki appliance port binary sensor."""

    coordinator: MerakiApplianceCoordinator

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiApplianceCoordinator,
        device: MerakiDevice,
        port: MerakiAppliancePort,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_serial = str(device.serial)
        self._port = port
        self._attr_unique_id = f"{device.serial}_port_{self._port.number}_connectivity"
        self._attr_name = f"Port {self._port.number}"
        self._last_state = None


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator, deduplicating unchanged states."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            appliance_ports = getattr(device, "appliance_ports", [])
            if not isinstance(appliance_ports, list):
                return

            for port in appliance_ports:
                # Defensive check: ensure port and its number attribute exist
                if port is None or getattr(port, "number", None) is None:
                    continue
                if port.number == self._port.number:
                    self._port = port

                    # Only trigger an expensive UI write if the status actually changed
                    current_state = self.is_on
                    if self._last_state != current_state:
                        self._last_state = current_state
                        self.async_write_ha_state()
                    return

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if not self._port or not getattr(self._port, "enabled", False):
            return False
        return (
            self._port.status is not None and self._port.status.lower() == "connected"
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_number": self._port.number,
            "link_speed": self._port.speed,
            "vlan": self._port.vlan,
            "type": self._port.type,
        }
