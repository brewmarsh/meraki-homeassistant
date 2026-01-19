"""
Base Device Handler.

This module defines the BaseDeviceHandler class, which provides a common
interface for all device-specific handlers.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
    from ....core.coordinators.meraki_data_coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
=======
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
<<<<<<< HEAD
=======
    from ...meraki_data_coordinator import (
        MerakiDataCoordinator,
    )
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)


_LOGGER = logging.getLogger(__name__)


class BaseHandler(ABC):
    """Base class for entity handlers."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the BaseHandler."""
        self._coordinator = coordinator
        self._config_entry = config_entry

    @abstractmethod
    async def discover_entities(self) -> list[Entity]:
        """Discover entities."""
        raise NotImplementedError("Subclasses must implement discover_entities")


class BaseDeviceHandler(BaseHandler, ABC):
    """Base class for device-specific entity handlers."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the BaseDeviceHandler."""
        super().__init__(coordinator, config_entry)
        self.device = device

    @classmethod
    @abstractmethod
    def create(
        cls,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    ) -> BaseDeviceHandler:
        """Create an instance of the handler."""
        raise NotImplementedError
