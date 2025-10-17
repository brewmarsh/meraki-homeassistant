"""
Device handler for Meraki GX appliances.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...button.reboot import MerakiRebootButton
from ...sensor.device.appliance_uplink import MerakiApplianceUplinkSensor

if TYPE_CHECKING:
    from homeassistant.helpers.entity import Entity
    from ....types import MerakiDevice
    from ....core.coordinators.meraki_data_coordinator import MerakiDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ....services.camera_service import CameraService
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class GXHandler(BaseDeviceHandler):
    """Handler for GX series security appliances."""

    def __init__(
        self,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the GXHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "GXHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for the device."""
        entities: List[Entity] = []
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
