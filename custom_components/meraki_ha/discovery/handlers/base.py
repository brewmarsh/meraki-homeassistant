"""
Base Device Handler

This module defines the BaseDeviceHandler class, which provides a common
interface for all device-specific handlers.
"""
from __future__ import annotations
from abc import ABC, abstractmethod

import logging
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ....types import MerakiDevice
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class BaseDeviceHandler(ABC):
    """Base class for device-specific entity handlers."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
    ) -> None:
        """Initialize the BaseDeviceHandler."""
        self._coordinator = coordinator
        self.device = device
        self._config_entry = config_entry

    @classmethod
    @abstractmethod
    def create(
        cls,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "BaseDeviceHandler":
        """Create an instance of the handler."""
        raise NotImplementedError

    async def discover_entities(self) -> List[Entity]:
        """
        Discover entities for the device.

        This method should be implemented by subclasses to return a list
        of entities for the specific device type.
        """
        raise NotImplementedError("Subclasses must implement discover_entities")
