"""Switch for controlling Meraki device LEDs."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models.device import MerakiDevice
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceLEDSwitch(CoordinatorEntity, SwitchEntity):
    """Switch for controlling Meraki device LEDs."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True
    _attr_icon = "mdi:led-on"

    coordinator: MerakiDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_led_control"
        self._attr_name = "LED Control"

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
        )
        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this switch's device from the coordinator."""
        if self._device_serial:
            return self.coordinator.get_device(self._device_serial)
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the switch."""
        # Prevent state overwrite during optimistic update
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return

        device = self._get_current_device_data()
        if device and device.management_interface:
            self._attr_is_on = device.management_interface.get("ledLights", True)
        else:
            self._attr_is_on = True  # Default to on

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the LEDs on."""
        await self._async_set_led_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the LEDs off."""
        await self._async_set_led_state(False)

    async def _async_set_led_state(self, enabled: bool) -> None:
        """Update the LED state via API."""
        if not self._device_serial:
            return

        # Optimistic update
        self._attr_is_on = enabled
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self.coordinator.api.devices.update_device_management_interface(
                serial=self._device_serial,
                ledLights=enabled,
            )
        except Exception as e:
            _LOGGER.error(
                "Failed to update LED state for %s: %s", self._device_serial, e
            )
            # Revert optimistic update
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self._update_state()
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
