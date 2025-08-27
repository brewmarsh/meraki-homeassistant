"""
Network Handler

This module defines the NetworkHandler class, which is responsible for
discovering and creating network-level entities.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...sensor.network.network_clients import MerakiNetworkClientsSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class NetworkHandler(BaseDeviceHandler):
    """Handler for network-level entities."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the NetworkHandler."""
        # This handler is not device-specific, so we pass None for the device.
        super().__init__(coordinator, device=None, config_entry=config_entry, camera_service=None)
        self._network_control_service = network_control_service

    async def discover_entities(self) -> List["Entity"]:
        """Discover network-level entities."""
        entities = []
        networks = self._coordinator.data.get("networks", [])
        if not networks:
            _LOGGER.debug("No networks found to create network-level entities.")
            return entities

        for network in networks:
            entities.append(
                MerakiNetworkClientsSensor(
                    coordinator=self._coordinator,
                    config_entry=self._config_entry,
                    network_data=network,
                    network_control_service=self._network_control_service,
                )
            )
        _LOGGER.info("Discovered %d network-level entities", len(entities))
        return entities
