"""Sensor for Meraki appliance data usage."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import UnitOfInformation
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUsageSensor(CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity):
    """Representation of a Meraki appliance data usage sensor.

    This sensor displays the total data usage for a Meraki MX appliance
    over the last day. The state is the total data usage in megabytes,
    and the attributes provide a breakdown of sent and received data.
    """

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfInformation.MEGABYTES
    _attr_icon = "mdi:chart-bar"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_data_usage"
        self._attr_name = f"{self._device['name']} Data Usage"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        traffic = self._device.get("traffic")
        if not traffic or not isinstance(traffic, list) or not traffic[0]:
            return None
        # The API returns a list of dictionaries, one for each traffic type
        # We are interested in the total traffic, which is the sum of sent and received
        total_kb = traffic[0].get("received", 0) + traffic[0].get("sent", 0)
        return round(total_kb / 1024, 2) # Convert to MB

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        traffic = self._device.get("traffic")
        if not traffic or not isinstance(traffic, list) or not traffic[0]:
            return {}

        return {
            "sent": round(traffic[0].get("sent", 0) / 1024, 2),
            "received": round(traffic[0].get("received", 0) / 1024, 2),
            "timespan_seconds": 86400, # Hardcoded for now
        }
