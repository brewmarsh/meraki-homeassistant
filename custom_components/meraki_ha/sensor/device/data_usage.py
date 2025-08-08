"""Sensor for Meraki appliance data usage."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiDataUsageSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a Meraki appliance data usage sensor."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfInformation.MEGABYTES
    _attr_icon = "mdi:chart-bar"
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._network_id: str = device_data["networkId"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_data_usage"
        self._attr_name = "Data Usage"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            sw_version=device_data.get("firmware"),
        )
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if (
            not self.coordinator.data
            or "appliance_traffic" not in self.coordinator.data
        ):
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return

        traffic_data = self.coordinator.data["appliance_traffic"].get(self._network_id)
        if not traffic_data or not isinstance(traffic_data, list):
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return

        total_sent_kb = sum(item.get("sent", 0) for item in traffic_data)
        total_recv_kb = sum(item.get("recv", 0) for item in traffic_data)
        total_kb = total_sent_kb + total_recv_kb

        self._attr_native_value = round(total_kb / 1024, 2)  # Convert to MB

        self._attr_extra_state_attributes = {
            "sent_mb": round(total_sent_kb / 1024, 2),
            "received_mb": round(total_recv_kb / 1024, 2),
            "timespan_seconds": 86400,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            super().available
            and self.coordinator.data
            and "appliance_traffic" in self.coordinator.data
            and self._network_id in self.coordinator.data["appliance_traffic"]
        )
