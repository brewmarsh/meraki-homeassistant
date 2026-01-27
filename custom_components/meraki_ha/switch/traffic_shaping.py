"""Switch for Meraki Traffic Shaping."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.entities.meraki_network_entity import MerakiNetworkEntity
from ..types import MerakiTrafficShaping

_LOGGER = logging.getLogger(__name__)


class MerakiTrafficShapingSwitch(MerakiNetworkEntity, SwitchEntity):
    """Representation of a Meraki Traffic Shaping switch."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        traffic_shaping: MerakiTrafficShaping,
    ) -> None:
        """
        Initialize the switch.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            network_id: The ID of the network.
            traffic_shaping: The traffic shaping settings.

        """
        # We need the network object for MerakiNetworkEntity
        network = coordinator.get_network(network_id)
        if not network:
            # Should not happen if set up correctly
            raise ValueError(f"Network {network_id} not found")

        super().__init__(coordinator, config_entry, network)
        self._traffic_shaping = traffic_shaping
        self._attr_unique_id = f"{network_id}_traffic_shaping_switch"
        self._attr_name = "Traffic Shaping"
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        self._attr_is_on = self._traffic_shaping.enabled

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        traffic_shaping_by_network = self.coordinator.data.get("traffic_shaping", {})
        if self._network_id in traffic_shaping_by_network:
            self._traffic_shaping = traffic_shaping_by_network[self._network_id]
            self._update_internal_state()
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the switch on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        await self.coordinator.api.appliance.update_traffic_shaping(
            network_id=self._network_id,
            enabled=True,
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the switch off.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        await self.coordinator.api.appliance.update_traffic_shaping(
            network_id=self._network_id,
            enabled=False,
        )
