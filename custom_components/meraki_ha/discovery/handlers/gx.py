"""Discovery handler for GX devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...button.reboot import MerakiRebootButton
from ...sensor.device.appliance_uplink import MerakiApplianceUplinkSensor
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....types import MerakiDevice
    from ...meraki_data_coordinator import (
        MerakiDataCoordinator,
    )
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class GXHandler(BaseDeviceHandler):
    """Handler for GX series security appliances."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the GXHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service,  # Unused
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> GXHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the device."""
        entities: list[Entity] = []
        entities.append(
            MerakiRebootButton(self._control_service, self.device, self._config_entry)
        )
        # Add uplink sensors
        if self._coordinator.data and self._coordinator.data.get(
            "appliance_uplink_statuses"
        ):
            for status in self._coordinator.data["appliance_uplink_statuses"]:
                if status.get("serial") == self.device["serial"]:
                    for uplink in status.get("uplinks", []):
                        entities.append(
                            MerakiApplianceUplinkSensor(
                                coordinator=self._coordinator,
                                device_data=self.device,
                                config_entry=self._config_entry,
                                uplink_data=uplink,
                            )
                        )
        return entities
