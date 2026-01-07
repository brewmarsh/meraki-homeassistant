"""Meraki MG Cellular Gateway Handler."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...button.reboot import MerakiRebootButton
from ...const import CONF_ENABLE_DEVICE_STATUS
from ...sensor.device.cellular_uplink import (
    MerakiCellularSignalSensor,
    MerakiCellularUplinkSensor,
)
from ...sensor.device.device_status import MerakiDeviceStatusSensor
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MGHandler(BaseDeviceHandler):
    """Handler for Meraki MG Cellular Gateways."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MGHandler."""
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
    ) -> MGHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the MG cellular gateway."""
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

        # Cellular uplink status sensor (shows status, provider, connection type)
        entities.append(
            MerakiCellularUplinkSensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        # Cellular signal strength sensor (RSRP in dBm)
        entities.append(
            MerakiCellularSignalSensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        return entities
