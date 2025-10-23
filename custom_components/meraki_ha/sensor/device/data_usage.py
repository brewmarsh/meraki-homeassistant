"""Sensor for Meraki appliance data usage."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiDataUsageSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki appliance data usage sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfInformation.MEGABYTES
    _attr_icon = "mdi:chart-bar"
    _attr_has_entity_name = True
    _attr_extra_state_attributes: Dict[str, Any] = {}

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        traffic_data = (
            self.coordinator.data.get("appliance_traffic", {}).get(self._network_id)
            if self.coordinator.data
            else None
        )

        if not traffic_data or (
            isinstance(traffic_data, dict) and traffic_data.get("error") == "disabled"
        ):
            self._attr_native_value = "Disabled"
            self._attr_extra_state_attributes = {
                "reason": "Traffic analysis is not enabled for this network."
            }
            self._attr_state_class = None
            self._attr_native_unit_of_measurement = None
            return

        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfInformation.MEGABYTES

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
        # This sensor should be available even if traffic analysis is disabled
        # so it can show the "Disabled" state.
        return super().available and self._get_current_device_data() is not None
