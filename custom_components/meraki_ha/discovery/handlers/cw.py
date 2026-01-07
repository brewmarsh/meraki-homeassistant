"""Catalyst CW Wireless Handler."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...button.reboot import MerakiRebootButton
from ...const import CONF_ENABLE_DEVICE_STATUS
from ...sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor
from ...sensor.device.device_status import MerakiDeviceStatusSensor
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


class CWHandler(BaseDeviceHandler):
    """Handler for Catalyst CW Wireless Access Points."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the CWHandler."""
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
    ) -> CWHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the CW wireless access point."""
        entities: list[Entity] = []

        # Reboot button
        entities.append(
            MerakiRebootButton(self._control_service, self.device, self._config_entry)
        )

        # Device status sensor
        if self._config_entry.options.get(CONF_ENABLE_DEVICE_STATUS, True):
            entities.append(
                MerakiDeviceStatusSensor(
                    self._coordinator, self.device, self._config_entry
                )
            )

        # Connected clients sensor
        entities.append(
            MerakiDeviceConnectedClientsSensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        return entities
