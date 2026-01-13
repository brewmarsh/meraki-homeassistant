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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    from ....core.coordinators.meraki_data_coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
<<<<<<< HEAD
=======
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    from ...meraki_data_coordinator import (
        MerakiDataCoordinator,
    )
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    from ...meraki_data_coordinator import (
        MerakiDataCoordinator,
    )
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


_LOGGER = logging.getLogger(__name__)


class BaseHandler(ABC):
    """Base class for entity handlers."""

    def __init__(
        self,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
<<<<<<< HEAD
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    ) -> BaseDeviceHandler:
        """Create an instance of the handler."""
        raise NotImplementedError
