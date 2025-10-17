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
    from ....core.coordinators.meraki_data_coordinator import MerakiDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class BaseHandler(ABC):
    """Base class for entity handlers."""

    def __init__(
        self,
        coordinator: "MerakiDataUpdateCoordinator",
        config_entry: "ConfigEntry",
    ) -> None:
        """Initialize the BaseHandler."""
        self._coordinator = coordinator
        self._config_entry = config_entry

    @abstractmethod
    async def discover_entities(self) -> List[Entity]:
        """Discover entities."""
        raise NotImplementedError("Subclasses must implement discover_entities")


class BaseDeviceHandler(BaseHandler, ABC):
    """Base class for device-specific entity handlers."""

    def __init__(
        self,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
    ) -> None:
        """Initialize the BaseDeviceHandler."""
        super().__init__(coordinator, config_entry)
        self.device = device

    @classmethod
    @abstractmethod
    def create(
        cls,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "BaseDeviceHandler":
        """Create an instance of the handler."""
        raise NotImplementedError
