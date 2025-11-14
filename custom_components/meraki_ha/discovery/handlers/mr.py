"""MR (Wireless) Device Handler."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


class MRHandler(BaseDeviceHandler):
    """Handler for Meraki MR (wireless) devices."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MRHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> MRHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for a wireless device."""
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
