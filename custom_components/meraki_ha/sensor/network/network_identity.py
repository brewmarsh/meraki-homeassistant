"""Sensor for Meraki network identity."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, MANUFACTURER
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkIdentitySensor(CoordinatorEntity, SensorEntity):
    """Sensor representing Meraki network identity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the network identity sensor."""
        super().__init__(coordinator)
        self._network_data = network_data
        self._config_entry = config_entry
        self._network_id = network_data.get("id", "")
        self._network_name = network_data.get("name", f"Network {self._network_id}")

        self._attr_unique_id = f"meraki_network_identity_{self._network_id}"
        self._attr_name = "Identity"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._network_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._network_id)},
            name=self._network_name,
            manufacturer=MANUFACTURER,
            model="Network",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "organization_id": self._network_data.get("organizationId"),
        }
