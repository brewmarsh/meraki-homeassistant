<<<<<<< HEAD
"""Discovery handler for MT devices."""
=======
<<<<<<< HEAD
"""Discovery handler for MT devices."""
=======
"""Device handler for Meraki MT sensors."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

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
    from ....services.camera_service import CameraService
    from ....services.network_control_service import NetworkControlService
<<<<<<< HEAD
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService
=======
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService
=======
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)


_LOGGER = logging.getLogger(__name__)


class MTHandler(BaseDeviceHandler):
    """Handler for MT series sensors."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MTHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service

    @classmethod
    def create(
        cls,
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
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
<<<<<<< HEAD
        network_control_service: NetworkControlService,
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
        network_control_service,  # Unused
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    ) -> MTHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the device."""
        entities: list[Entity] = []
        return entities
