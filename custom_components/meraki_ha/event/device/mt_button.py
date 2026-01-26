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
    """Representation of a Meraki MT button press event."""

    _attr_device_class = EventDeviceClass.BUTTON
    _attr_event_types = ["short_press", "long_press"]

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
        self._attr_unique_id = f"{device.serial}_button_event"
        self._attr_name = "Button Press"
        self._last_ts: str | None = None
        self._is_first_update = True

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    def _update_from_device(self) -> None:
        """Update the entity from device data."""
        button_data = self._device.button_press
        if not button_data:
            return

        ts = button_data.get("ts")
        press_type = button_data.get("pressType")

        if not ts or not press_type:
            return

        # If it's the first update, just store the timestamp to avoid triggering
        # old events
        if self._is_first_update:
            self._last_ts = ts
            self._is_first_update = False
            return

        if ts != self._last_ts:
            self._last_ts = ts
            event_type = f"{press_type}_press"
            if event_type in self._attr_event_types:
                self._trigger_event(event_type, {"press_type": press_type, "ts": ts})
            else:
                _LOGGER.warning(
                    "Unknown press type '%s' for device %s",
                    press_type,
                    self._device.serial,
                )

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        # Initialize with current state to prevent triggering on startup
        button_data = self._device.button_press
        if button_data and (ts := button_data.get("ts")):
            self._last_ts = ts
        self._is_first_update = False

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            self._update_from_device()
        super()._handle_coordinator_update()
