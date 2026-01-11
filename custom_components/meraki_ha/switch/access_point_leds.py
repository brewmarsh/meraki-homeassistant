"""Switch for a Meraki network's access point LEDs."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..core.entities.meraki_network_entity import MerakiNetworkEntity
from ..helpers.logging_helper import MerakiLoggers
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..types import MerakiNetwork

_LOGGER = MerakiLoggers.SWITCH


class MerakiAPLEDSwitch(MerakiNetworkEntity, SwitchEntity):
    """Representation of a Meraki network's access point LED switch."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, config_entry, network)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a network entity")

        self._attr_unique_id = f"meraki_{self._network_id}_ap_leds"
        self._attr_name = "Access Point LEDs"
        self._update_internal_state()

    def _get_wireless_settings(self) -> dict[str, Any] | None:
        """Get wireless settings for this network from the coordinator."""
        return self.coordinator.data.get("wireless_settings", {}).get(self._network_id)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._get_wireless_settings() is not None

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return

        if wireless_settings := self._get_wireless_settings():
            self._attr_is_on = wireless_settings.get("ledLightsOn")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        await self.coordinator.api.wireless.update_network_wireless_settings(
            network_id=self._network_id, ledLightsOn=True
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        await self.coordinator.api.wireless.update_network_wireless_settings(
            network_id=self._network_id, ledLightsOn=False
        )
