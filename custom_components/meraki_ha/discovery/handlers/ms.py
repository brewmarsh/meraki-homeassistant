"""Meraki MS Switch Handler."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

<<<<<<< HEAD
<<<<<<< HEAD
=======
from ...const import CONF_ENABLE_PORT_SENSORS
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from ...const import CONF_ENABLE_PORT_SENSORS
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> MSHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the MS switch."""
        from ...binary_sensor.switch_port import SwitchPortSensor

        entities: list[Entity] = []
<<<<<<< HEAD
<<<<<<< HEAD
        if self.device and self.device.get("ports_statuses"):
            for port in self.device["ports_statuses"]:
                entities.append(SwitchPortSensor(self._coordinator, self.device, port))
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

        # Check if port sensors are enabled
        if self._config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            if self.device and self.device.get("ports_statuses"):
                for port in self.device["ports_statuses"]:
                    entities.append(
                        SwitchPortSensor(self._coordinator, self.device, port)
                    )
        else:
            _LOGGER.debug(
                "Port sensors disabled for device %s", self.device.get("serial")
            )

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        return entities
