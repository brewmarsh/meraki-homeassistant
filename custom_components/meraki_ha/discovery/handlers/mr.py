<<<<<<< HEAD
"""MR (Wireless) Device Handler."""
=======
"""
MR (Wireless) Device Handler.

This module defines the MRHandler class, which is responsible for discovering
entities for Meraki MR series (wireless) devices.
"""
>>>>>>> origin/beta

from __future__ import annotations

import logging
<<<<<<< HEAD
from typing import TYPE_CHECKING
=======
from typing import TYPE_CHECKING, Any
>>>>>>> origin/beta

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.device_control_service import DeviceControlService
=======
    from ....coordinator import MerakiDataUpdateCoordinator
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
>>>>>>> origin/beta


_LOGGER = logging.getLogger(__name__)


class MRHandler(BaseDeviceHandler):
    """Handler for Meraki MR (wireless) devices."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MRHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
    ) -> None:
        """
        Initialize the MRHandler.

        Args:
            coordinator: The data update coordinator.
            device: The device data.
            config_entry: The config entry.
            control_service: The device control service.

        """
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
>>>>>>> origin/beta

    @classmethod
    def create(
        cls,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service,  # Unused
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> MRHandler:
        """Create an instance of the handler."""
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        switch_port_coordinator: Any,
    ) -> MRHandler:
        """
        Create an instance of the handler.

        Args:
            coordinator: The data update coordinator.
            device: The device data.
            config_entry: The config entry.
            camera_service: The camera service.
            control_service: The device control service.
            network_control_service: The network control service.
            switch_port_coordinator: The switch port coordinator.

        """
>>>>>>> origin/beta
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
<<<<<<< HEAD
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for a wireless device."""
=======
        )

    async def discover_entities(self) -> list[Entity]:
        """
        Discover entities for a wireless device.

        Returns
        -------
            A list of entities.

        """
>>>>>>> origin/beta
        entities: list[Entity] = []

        # In the future, this is where we would create entities like:
        # - Radio settings sensors
        # - Connected client count sensors
        # - etc.
        #
        # For example:
        # if "radio_settings" in self.device:
        #     entities.append(RadioSettingsSensor(self.device))

        return entities
