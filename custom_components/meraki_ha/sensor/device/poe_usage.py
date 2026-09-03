"""Sensor for Meraki switch PoE usage."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import UnitOfPower
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...entity import MerakiSensor

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiPoeUsageSensor(MerakiSensor):
    """
    Representation of a Meraki switch PoE usage sensor.

    This sensor displays the aggregated PoE usage for a Meraki MS switch
    in watts. The attributes provide a breakdown of PoE usage per port.
    """

    coordinator: MerakiMainCoordinator

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_icon = "mdi:power-plug"

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            device: The device data.

        """
        super().__init__(coordinator)
        self._device = device
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{device.serial}_poe_usage"
        self._attr_name = "PoE Usage"
        self._update_state()

    def _update_state(self) -> None:
        """Update the sensor state and attributes in a single pass."""
        ports_statuses = self._device.switch_ports
        if not isinstance(ports_statuses, list):
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return

        total_poe_usage_wh = 0
        attrs = {}

        for port in ports_statuses:
            if isinstance(port, dict):
                usage = port.get("powerUsageInWh", 0) or 0
                total_poe_usage_wh += usage
                if "portId" in port:
                    attr_key = f"port_{port['portId']}_power_usage_wh"
                    attrs[attr_key] = port.get("powerUsageInWh")

        if total_poe_usage_wh > 0:
            self._attr_native_value = round(total_poe_usage_wh / 24, 2)
        else:
            self._attr_native_value = 0.0

        self._attr_extra_state_attributes = attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._device.serial:
            device = self.coordinator.get_device(self._device.serial)
            if device:
                self._device = device
                self._update_state()
                self.async_write_ha_state()
