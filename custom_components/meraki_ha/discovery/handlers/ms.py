"""
Meraki MS Switch Handler

This module defines the MSHandler class, which is responsible for discovering
entities for Meraki MS switches.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...binary_sensor.switch_port import SwitchPortSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ....core.coordinators.switch_port_status_coordinator import SwitchPortStatusCoordinator
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        control_service: "DeviceControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._switch_port_coordinator = switch_port_coordinator

    def discover_entities(self) -> List[Entity]:
        """Discover entities for the MS switch."""
        _LOGGER.debug("Discovering entities for MS switch %s", self.device["serial"])
        entities = []
        ports = self.device.get("ports_statuses", [])
        for port in ports:
            entities.append(
                SwitchPortSensor(self._switch_port_coordinator, self.device, port)
            )
        return entities
