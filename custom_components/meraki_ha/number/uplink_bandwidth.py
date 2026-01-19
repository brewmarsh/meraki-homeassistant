"""Number entities for Meraki uplink bandwidth."""

from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..core.entities.meraki_network_entity import MerakiNetworkEntity
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..types import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class MerakiUplinkBandwidthNumber(MerakiNetworkEntity, NumberEntity):
    """Representation of a Meraki uplink bandwidth number."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
        uplink: str,
        direction: str,
    ) -> None:
        """Initialize the number."""
        super().__init__(coordinator, config_entry, network)
        self._uplink = uplink
        self._direction = direction
        self._attr_unique_id = (
            f"uplink_bandwidth_{self._network_id}_{self._uplink}_{self._direction}"
        )
        self._attr_name = (
            f"{self._network.name} {self._uplink.capitalize()} "
            f"{self._direction.capitalize()} Limit"
        )
        self._attr_native_unit_of_measurement = "kbps"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 1000000
        self._attr_native_step = 1
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the number."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        traffic_shaping = self.coordinator.data.get("traffic_shaping", {}).get(
            self._network_id, {}
        )
        if traffic_shaping:
            limits = traffic_shaping.get("bandwidthLimits", {})
            uplink_limits = limits.get(self._uplink, {})
            value = uplink_limits.get(f"limit{self._direction.capitalize()}")
            self._attr_native_value = float(value) if value is not None else None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        traffic_shaping = self.coordinator.data.get("traffic_shaping", {}).get(
            self._network_id, {}
        )
        if traffic_shaping:
            limits = traffic_shaping.get("bandwidthLimits", {})
            if self._uplink not in limits:
                limits[self._uplink] = {}
            limits[self._uplink][f"limit{self._direction.capitalize()}"] = int(value)
            await self.coordinator.api.appliance.update_traffic_shaping(
                network_id=self._network_id, bandwidthLimits=limits
            )
