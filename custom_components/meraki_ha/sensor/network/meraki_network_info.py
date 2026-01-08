"""Sensor for Meraki network information."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, MANUFACTURER
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing Meraki network information."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the network info sensor."""
        super().__init__(coordinator)
        self._network_data = network_data
        self._config_entry = config_entry
        self._network_id = network_data.get("id", "")
        self._network_name = network_data.get("name", f"Network {self._network_id}")

        self._attr_unique_id = f"{self._network_id}_network_info"
        self._attr_name = "Network Info"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._network_name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Create device data for naming with network product type
        device_data = {
            "name": self._network_name,
            "productTypes": self._network_data.get("productTypes", []),
        }
        formatted_name = format_device_name(device_data, self._config_entry.options)
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{self._network_id}")},
            name=formatted_name,
            manufacturer=MANUFACTURER,
            model="Network",
            configuration_url=f"https://dashboard.meraki.com/n/{self._network_id}",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "network_id": self._network_id,
            "network_type": self._network_data.get("productTypes", []),
            "time_zone": self._network_data.get("timeZone"),
            "tags": self._network_data.get("tags", []),
        }
