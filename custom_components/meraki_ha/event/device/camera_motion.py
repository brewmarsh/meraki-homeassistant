"""Event entity for Meraki camera motion detection."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

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
    from ...services.camera_service import CameraService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MerakiCameraMotionEvent(MerakiEntity, EventEntity):
    """Representation of a camera motion event."""

    _attr_device_class = EventDeviceClass.MOTION
    _attr_event_types = ["motion", "person", "vehicle"]

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the event entity."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{device.serial}-motion-event"
        self._attr_name = "Motion Event"
        self._last_timestamp: float = 0
        self._is_first_update = True

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def should_poll(self) -> bool:
        """Return True to enable polling."""
        return True

    async def async_update(self) -> None:
        """Update the entity."""
        try:
            motion_events = await self._camera_service.get_motion_history(
                str(self._device.serial)
            )
        except Exception as e:
            _LOGGER.error(
                "Error updating motion event for %s: %s", str(self._device.serial), e
            )
            return

        if not motion_events:
            self._is_first_update = False
            return

        # Sort events by startTs
        motion_events.sort(key=lambda x: x.get("startTs", 0))

        if self._is_first_update:
            if motion_events:
                # Initialize to the last event timestamp so we don't replay history
                self._last_timestamp = motion_events[-1].get("startTs", 0)
            self._is_first_update = False
            return

        for event in motion_events:
            start_ts = event.get("startTs", 0)
            if start_ts > self._last_timestamp:
                self._last_timestamp = start_ts
                event_type = event.get("event_type", "motion")
                # EventEntity expects event_type to be one of _attr_event_types
                if event_type not in self._attr_event_types:
                    event_type = "motion"

                self._trigger_event(event_type, event)
