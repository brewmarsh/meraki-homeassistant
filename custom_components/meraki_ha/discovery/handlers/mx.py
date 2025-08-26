"""
Device handler for Meraki MX appliances.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...button import MerakiRebootButton

if TYPE_CHECKING:
    from homeassistant.helpers.entity import Entity
    from ....types import MerakiDevice
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ...services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


class MXHandler(BaseDeviceHandler):
    """Handler for MX series security appliances."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MXHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service

    def discover_entities(self) -> List[Entity]:
        """Discover entities for the device."""
        entities: List[Entity] = []
        _LOGGER.debug("Discovering entities for MX device %s", self.device["serial"])
        entities.append(
            MerakiRebootButton(self._control_service, self.device, self._config_entry)
        )
        return entities
