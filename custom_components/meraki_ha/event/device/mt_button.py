"""Event entity for Meraki MT button press."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.event import (
    EventDeviceClass,
    EventEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MerakiMtButtonEvent(MerakiEntity, EventEntity):
    """Representation of an MT button press event."""

    _attr_device_class = EventDeviceClass.BUTTON
    _attr_event_types = ["short_press", "long_press"]
    _attr_translation_key = "button_press"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the event entity."""
        super().__init__(coordinator)
        self._device = device
        self._config_entry = config_entry
        self._attr_unique_id = f"{device.serial}-button-event"
        self._last_ts: str = ""

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to Home Assistant."""
        await super().async_added_to_hass()
        # Initialize last timestamp to prevent replaying old events
        device = self.coordinator.get_device(self._device.serial)
        if device and device.button_press:
            self._last_ts = device.button_press.get("ts", "")

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Get the latest device data
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device

            if device.button_press:
                ts = device.button_press.get("ts", "")
                if ts and ts != self._last_ts:
                    self._last_ts = ts
                    self._trigger(device.button_press)

        super()._handle_coordinator_update()

    def _trigger(self, button_press: dict[str, Any]) -> None:
        """Trigger the event."""
        press_type = button_press.get("pressType", "short")
        event_type = "short_press"
        if press_type == "long":
            event_type = "long_press"
        elif press_type == "short":
            event_type = "short_press"
        else:
            # Fallback or log warning?
            # Assuming 'short' as default for safety, or we could skip?
            # Meraki docs say 'short' or 'long'.
            pass

        if event_type in self._attr_event_types:
            self._trigger_event(event_type)
            self.async_write_ha_state()
