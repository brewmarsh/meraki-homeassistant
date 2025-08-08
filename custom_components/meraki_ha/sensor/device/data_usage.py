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

    def _get_current_device_data(self) -> Dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()
        traffic = current_device_data.get("traffic") if current_device_data else None

        if not traffic or not isinstance(traffic, list) or not traffic[0]:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
            return

        total_kb = traffic[0].get("received", 0) + traffic[0].get("sent", 0)
        self._attr_native_value = round(total_kb / 1024, 2)

        self._attr_extra_state_attributes = {
            "sent_mb": round(traffic[0].get("sent", 0) / 1024, 2),
            "received_mb": round(traffic[0].get("received", 0) / 1024, 2),
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
        return super().available and self._get_current_device_data() is not None
