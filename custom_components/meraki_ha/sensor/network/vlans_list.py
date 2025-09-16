"""Sensor for a list of Meraki VLANs."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinator import MerakiDataUpdateCoordinator
from .network_base import MerakiNetworkBaseSensor

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkVLANsSensor(MerakiNetworkBaseSensor):
    """Representation of a Meraki network's VLANs sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data, "vlans")
        self._attr_name = f"{network_data['name']} VLANs"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        vlans = self.coordinator.data.get("vlans", {}).get(self._network_id, [])
        self._attr_native_value = len(vlans)
        self._attr_extra_state_attributes = {"vlans": vlans}
        self.async_write_ha_state()
