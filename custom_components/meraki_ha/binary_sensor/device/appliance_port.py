"""Binary sensor for Meraki appliance port status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.models import MerakiAppliancePort
from ...core.models.device import MerakiDevice
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...coordinators import MerakiApplianceCoordinator


class AppliancePortBinarySensor(CoordinatorEntity, BinarySensorEntity):
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
        self._port = port
        self._attr_unique_id = f"{device.serial}_port_{self._port.number}_connectivity"
        self._attr_name = f"Port {self._port.number}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        if self.coordinator.config_entry:
            format_device_name(self._device, self.coordinator.config_entry.options)
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
            name=format_device_name(
                self._device,
                self.coordinator.config_entry.options
                if self.coordinator.config_entry
                else {},
            ),
            model=getattr(self._device, "model", None)
            if not isinstance(self._device, dict)
            else self._device.get("model"),
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            appliance_ports = getattr(device, "appliance_ports", [])
            if not isinstance(appliance_ports, list):
                return

            for port in appliance_ports:
                if not hasattr(port, "number"):
                    continue
                if port.number == self._port.number:
                    self._port = port
                    self.async_write_ha_state()
                    return

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if not self._port.enabled:
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
