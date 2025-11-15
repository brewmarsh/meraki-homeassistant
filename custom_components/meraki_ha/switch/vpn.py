"""Switch for Meraki Site-to-Site VPN."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..meraki_data_coordinator import MerakiDataCoordinator
from ..core.entities.meraki_network_entity import MerakiNetworkEntity
from ..types import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class MerakiVPNSwitch(MerakiNetworkEntity, SwitchEntity):
    """Representation of a Meraki Site-to-Site VPN switch."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        """
        Initialize the switch.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            network: The network data.

        """
        super().__init__(coordinator, config_entry, network)
        self._attr_unique_id = f"vpn_{self._network_id}"
        self._attr_name = "Site-to-Site VPN"
        self._attr_has_entity_name = True
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        if self._network_id in self.coordinator.data.get("vpn_status", {}):
            vpn_status = self.coordinator.data["vpn_status"][self._network_id]
            if vpn_status:
                self._attr_is_on = vpn_status.get("mode") != "disabled"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
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
        if self._network_id:
            await self.coordinator.api.appliance.update_vpn_status(
                network_id=self._network_id,
                mode="hub",
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
        if self._network_id:
            await self.coordinator.api.appliance.update_vpn_status(
                network_id=self._network_id,
                mode="disabled",
            )
