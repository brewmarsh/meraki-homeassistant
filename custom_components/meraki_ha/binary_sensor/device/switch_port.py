"""Binary sensor for Meraki switch port status."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.core import callback

from ...coordinators import MerakiSwitchCoordinator
from ...core.models.device import MerakiDevice
from ...entity import MerakiBinarySensor


class SwitchPortSensor(MerakiBinarySensor):
    """Representation of a Meraki switch port sensor."""

    coordinator: MerakiSwitchCoordinator

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        port: dict[str, Any] | Any,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_serial = str(device.serial)
        if hasattr(port, "to_dict"):
            self._port = port.to_dict()
        else:
            self._port = port

        # MX appliances use 'number', MS switches use 'portId'
        port_id = self._port.get("portId") or self._port.get("number")

        # Legacy Unique ID format to prevent breaking changes
        self._attr_unique_id = f"{device.serial}_{port_id}"
        self._attr_name = f"Port {port_id}"
        self._last_state = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator, deduplicating unchanged states."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            switch_ports = getattr(device, "switch_ports", [])
            appliance_ports = getattr(device, "appliance_ports", [])
            ports = (switch_ports if isinstance(switch_ports, list) else []) or (
                appliance_ports if isinstance(appliance_ports, list) else []
            )
            for port_data in ports:
                if port_data is None or isinstance(port_data, str):
                    continue
                if hasattr(port_data, "to_dict"):
                    port = port_data.to_dict()
                else:
                    port = port_data  # type: ignore[assignment]

                port_id = self._port.get("portId") or self._port.get("number")
                if port.get("portId") == port_id or port.get("number") == port_id:
                    self._port = port

                    # Action 2: Only trigger an expensive UI write if
                    # the port status actually changed
                    current_state = self.is_on
                    if self._last_state != current_state:
                        self._last_state = current_state
                        self.async_write_ha_state()
                    return

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if not self._port.get("enabled", True):
            return False

        status = self._port.get("status", "")
        return status is not None and status.lower() == "connected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        port_id = self._port.get("portId") or self._port.get("number")
        return {
            "name": self._port.get("name"),
            "port_id": port_id,
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "type": self._port.get("type"),
            "poe_enabled": self._port.get("poeEnabled"),
            "enabled": self._port.get("enabled"),
        }
