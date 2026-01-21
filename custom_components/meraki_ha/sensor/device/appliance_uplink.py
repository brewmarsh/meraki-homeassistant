"""Sensor for Meraki appliance uplink status."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiApplianceUplinkSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki appliance uplink sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        uplink_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data.serial
        self._config_entry = config_entry
        self._uplink_interface: str = uplink_data["interface"]

        self._attr_unique_id = f"{self._device_serial}_uplink_{self._uplink_interface}"
        self._attr_name = f"Uplink {self._uplink_interface.upper()}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.model,
            manufacturer="Cisco Meraki",
        )
        self._update_state()

    def _get_current_uplink_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's uplink from the coordinator."""
        device = self.coordinator.get_device(self._device_serial)
        if device:
            for uplink in device.appliance_uplink_statuses:
                if uplink.get("interface") == self._uplink_interface:
                    return uplink
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        uplink_data = self._get_current_uplink_data()
        if uplink_data:
            self._attr_native_value = uplink_data.get("status")
            self._attr_extra_state_attributes = {
                "ip": uplink_data.get("ip"),
                "gateway": uplink_data.get("gateway"),
                "public_ip": uplink_data.get("public_ip"),
                "primary_dns": uplink_data.get("primary_dns"),
                "secondary_dns": uplink_data.get("secondary_dns"),
            }
            self._attr_icon = "mdi:wan" if self.native_value == "active" else "mdi:wan"
        else:
            self._attr_native_value = "unknown"
            self._attr_extra_state_attributes = {}
            self._attr_icon = "mdi:help-rhombus"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_uplink_data() is not None
