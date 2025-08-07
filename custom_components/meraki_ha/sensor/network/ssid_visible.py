"""Sensor entity representing the visibility of a Meraki SSID."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDVisibleSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki SSID Visibility sensor."""

    _attr_icon = "mdi:eye"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_id: str,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._network_id = network_id
        self._ssid_data = ssid_data

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        ssid_number = self._ssid_data.get("number")
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            ssid_name, "sensor", name_format, "Visible"
        )
        self._attr_unique_id = f"{self._network_id}_{ssid_number}_visible"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{self._network_id}_{ssid_number}")},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data = None
        if self.coordinator.data and "ssids" in self.coordinator.data:
            for ssid in self.coordinator.data["ssids"]:
                if ssid.get("networkId") == self._network_id and ssid.get("number") == self._ssid_data.get("number"):
                    current_ssid_data = ssid
                    break

        if current_ssid_data:
            self._ssid_data = current_ssid_data
            self._attr_native_value = self._ssid_data.get("visible")
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
