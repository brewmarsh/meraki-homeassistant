"""Switch entity for Meraki PoE switch ports."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import DOMAIN
from ..helpers.entity import MerakiDeviceEntity
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiPoESwitch(MerakiDeviceEntity, SwitchEntity):
    """Representation of a Meraki PoE switch port."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, device)
        self.config_entry = config_entry
        self._port = port
        self._attr_unique_id = f"{self.device['serial']}_{self._port['portId']}_poe"
        self._attr_name = f"Port {self._port['portId']} PoE"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._port.get("poeEnabled", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            await self.coordinator.api.switch.update_device_switch_port(
                serial=self.device["serial"],
                port_id=self._port["portId"],
                poeEnabled=True,
            )
            self._port["poeEnabled"] = True
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(
                "Failed to turn on PoE for port %s on device %s: %s",
                self._port["portId"],
                self.device["serial"],
                e,
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        try:
            await self.coordinator.api.switch.update_device_switch_port(
                serial=self.device["serial"],
                port_id=self._port["portId"],
                poeEnabled=False,
            )
            self._port["poeEnabled"] = False
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(
                "Failed to turn off PoE for port %s on device %s: %s",
                self._port["portId"],
                self.device["serial"],
                e,
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self.device["serial"]:
                    if device.get("ports_statuses"):
                        for port in device["ports_statuses"]:
                            if port.get("portId") == self._port["portId"]:
                                self._port = port
                                self.async_write_ha_state()
                                return
        super()._handle_coordinator_update()
