"""Discovery handler for MT devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...binary_sensor.device.meraki_mt_binary_base import MerakiMtBinarySensor
from ...descriptions import MT_BINARY_SENSOR_MODELS, MT_SENSOR_MODELS
from ...sensor.device.meraki_mt_base import MerakiMtSensor
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ....services.camera_service import CameraService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


class MTHandler(BaseDeviceHandler):
    """Handler for MT series sensors."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        switch_port_coordinator: SwitchPortStatusCoordinator,
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
        model = self.device.model
        if not model:
            return []

        # Look up supported sensors for this model
        sensor_descriptions = MT_SENSOR_MODELS.get(model)
        if sensor_descriptions:
            for description in sensor_descriptions:
                entities.append(
                    MerakiMtSensor(self._coordinator, self.device, description)
                )

        # Look up supported binary sensors for this model
        binary_sensor_descriptions = MT_BINARY_SENSOR_MODELS.get(model)
        if binary_sensor_descriptions:
            for binary_description in binary_sensor_descriptions:
                entities.append(
                    MerakiMtBinarySensor(
                        self._coordinator, self.device, binary_description
                    )
                )

        # If model is not explicitly mapped but starts with MT, we could try
        # to discover dynamic capabilities, but for now we stick to the
        # defined models as requested.

        return entities
