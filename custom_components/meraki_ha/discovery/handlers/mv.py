"""
MV (Camera) Device Handler

This module defines the MVHandler class, which is responsible for discovering
entities for Meraki MV series (camera) devices.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = logging.getLogger(__name__)


class MVHandler(BaseDeviceHandler):
    """Handler for Meraki MV (camera) devices."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: dict,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry)
        self._coordinator = coordinator
        self._config_entry = config_entry


    def discover_entities(self) -> List[Entity]:
        """Discover entities for a camera device."""
        _LOGGER.debug(
            "Discovering entities for MV device: %s", self.device.get("serial")
        )
        entities: List[Entity] = []

        if "video_settings" in self.device:
            from ...sensor.device.camera_rtsp_url import MerakiCameraRTSPUrlSensor

            entities.append(
                MerakiCameraRTSPUrlSensor(
                    self._coordinator,
                    self.device,
                    self._config_entry,
                )
            )
        return entities
