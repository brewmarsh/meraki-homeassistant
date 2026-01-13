<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
"""
MR (Wireless) Device Handler.

This module defines the MRHandler class, which is responsible for discovering
entities for Meraki MR series (wireless) devices.
"""
<<<<<<< HEAD
=======
=======
"""MR (Wireless) Device Handler."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
"""MR (Wireless) Device Handler."""
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

from __future__ import annotations

import logging
<<<<<<< HEAD
<<<<<<< HEAD
from typing import TYPE_CHECKING, Any
=======
<<<<<<< HEAD
from typing import TYPE_CHECKING, Any
=======
from typing import TYPE_CHECKING
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from typing import TYPE_CHECKING
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
<<<<<<< HEAD
    from ....coordinator import MerakiDataUpdateCoordinator
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
=======
<<<<<<< HEAD
    from ....coordinator import MerakiDataUpdateCoordinator
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.device_control_service import DeviceControlService
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


_LOGGER = logging.getLogger(__name__)


class MRHandler(BaseDeviceHandler):
    """Handler for Meraki MR (wireless) devices."""

    def __init__(
        self,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
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
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        coordinator: MerakiDataCoordinator,
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
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
<<<<<<< HEAD
=======
        self._network_control_service = network_control_service
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

    @classmethod
    def create(
        cls,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
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
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        coordinator: MerakiDataCoordinator,
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        switch_port_coordinator: Any,
    ) -> MRHandler:
<<<<<<< HEAD
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
=======
        """Create an instance of the handler."""
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
<<<<<<< HEAD
<<<<<<< HEAD
        )

    async def discover_entities(self) -> list[Entity]:
        """
        Discover entities for a wireless device.

        Returns
        -------
            A list of entities.

        """
=======
<<<<<<< HEAD
        )

    async def discover_entities(self) -> list[Entity]:
        """
        Discover entities for a wireless device.

        Returns
        -------
            A list of entities.

        """
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for a wireless device."""
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
