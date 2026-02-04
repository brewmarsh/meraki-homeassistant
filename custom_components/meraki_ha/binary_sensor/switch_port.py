"""Binary sensor for Meraki switch port status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ..types import MerakiAppliancePort, MerakiDevice

_LOGGER = logging.getLogger(__name__)


class SwitchPortSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki switch port sensor."""

    coordinator: MerakiDataUpdateCoordinator

    _attr_entity_registry_enabled_default = False
    _attr_state_color = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any] | MerakiAppliancePort,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        if hasattr(port, "to_dict"):
            self._port = port.to_dict()
        else:
            self._port = port

        # MX appliances use 'number', MS switches use 'portId'
        port_id = self._port.get("portId") or self._port.get("number")
        self._attr_unique_id = f"{device.serial}_{port_id}"
        self._attr_name = f"Port {port_id}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            ports = device.ports_statuses or device.appliance_ports or []
            for port_data in ports:
                if hasattr(port_data, "to_dict"):
                    port = port_data.to_dict()
                else:
                    port = port_data  # type: ignore[assignment]

                port_id = self._port.get("portId") or self._port.get("number")
                if port.get("portId") == port_id or port.get("number") == port_id:
                    self._port = port
                    self.async_write_ha_state()
                    return

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._port.get("status") == "Connected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        port_id = self._port.get("portId") or self._port.get("number")
        return {
            "port_id": port_id,
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "enabled": self._port.get("enabled"),
        }
