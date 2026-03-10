"""Sensor for Meraki switch PoE usage."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinators import MerakiMainCoordinator
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiPoeUsageSensor(
    CoordinatorEntity,
    SensorEntity,
):
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

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
            name=format_device_name(
                self._device,
                self.coordinator.config_entry.options,
            ),
            model=getattr(self._device, "model", None)
            if not isinstance(self._device, dict)
            else self._device.get("model"),
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._device.serial:
            device = self.coordinator.get_device(self._device.serial)
            if device:
                self._device = device
                self.async_write_ha_state()

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        ports_statuses = self._device.switch_ports
        if not isinstance(ports_statuses, list):
            return None

        total_poe_usage_wh = sum(
            port.get("powerUsageInWh", 0) or 0
            for port in ports_statuses
            if isinstance(port, dict)
        )

        # The API returns power usage in Wh over the last day.
        # We divide by 24 to get the average power in Watts.
        if total_poe_usage_wh > 0:
            return round(total_poe_usage_wh / 24, 2)
        return 0.0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        ports_statuses = self._device.switch_ports
        if not isinstance(ports_statuses, list):
            return {}

        return {
            f"port_{port['portId']}_power_usage_wh": port.get("powerUsageInWh")
            for port in ports_statuses
            if isinstance(port, dict) and "portId" in port
        }
