"""
MR (Wireless) Device Handler

This module defines the MRHandler class, which is responsible for discovering
entities for Meraki MR series (wireless) devices.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService
    from ....services.camera_service import CameraService
    from ....services.network_control_service import NetworkControlService
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class MRHandler(BaseDeviceHandler):
    """Handler for Meraki MR (wireless) devices."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        control_service: "DeviceControlService",
    ) -> None:
        """Initialize the MRHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service

    @classmethod
    def create(
        cls,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "MRHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for a wireless device."""
        entities: List[Entity] = []

        # In the future, this is where we would create entities like:
        # - Radio settings sensors
        # - Connected client count sensors
        # - etc.
        #
        # For example:
        # if "radio_settings" in self.device:
        #     entities.append(RadioSettingsSensor(self.device))

        return entities
