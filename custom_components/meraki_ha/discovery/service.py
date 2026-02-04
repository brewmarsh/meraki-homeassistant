"""
Device Discovery Service.

This module defines the DeviceDiscoveryService, which is responsible for
discovering devices from the Meraki data and delegating entity creation
to the appropriate handlers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..const_conf import (
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
)
from ..core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES
from ..core.models.device import MerakiDevice
from .handlers.network import NetworkHandler
from .handlers.ssid import SSIDHandler
from .handlers.universal import UniversalHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.api.client import MerakiAPIClient
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ..services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class DeviceDiscoveryService:
    """Service for discovering Meraki devices and creating corresponding entities."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service
        devices_data = self._coordinator.data.get("devices", [])
        self._devices: list[MerakiDevice] = [
            d if isinstance(d, MerakiDevice) else MerakiDevice.from_dict(d)
            for d in devices_data
        ]
        self.all_entities: list[Entity] = []

    async def discover_entities(self) -> list[Entity]:
        """
        Discover all entities for all devices and networks.

        This method iterates through all devices in the organization and uses
        the UniversalHandler to create entities based on device capabilities.
        It also discovers network-level and virtual SSID entities.
        """
        all_entities: list[Entity] = []

        # Discover network-level entities
        if self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            network_handler = NetworkHandler(
                self._coordinator,
                self._config_entry,
                self._network_control_service,
            )
            async for entity in network_handler.discover_entities():
                all_entities.append(entity)
        else:
            _LOGGER.debug("Network sensors are disabled.")

        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

        for device in self._devices:
            model = device.model
            if not model:
                _LOGGER.warning("Device %s has no model, skipping", device.serial)
                continue

            # Perform model-to-capability lookup
            capabilities = DEVICE_CAPABILITIES.get(model, DEFAULT_CAPS)

            # Use the UniversalHandler to create entities based on capabilities
            handler = UniversalHandler(
                self._coordinator,
                device,
                self._config_entry,
                capabilities,
                self._camera_service,
                self._control_service,
                self._network_control_service,
            )

            _LOGGER.debug(
                "Using UniversalHandler for %s (model: %s) with capabilities: %s",
                device.serial,
                model,
                capabilities,
            )

            async for entity in handler.discover_entities():
                all_entities.append(entity)

        # Create SSID handler for virtual SSID devices
        if self._config_entry.options.get(CONF_ENABLE_SSID_SENSORS, True):
            ssid_handler = SSIDHandler(
                self._coordinator, self._config_entry, self._meraki_client
            )
            async for entity in ssid_handler.discover_entities():
                all_entities.append(entity)
        else:
            _LOGGER.debug("SSID sensors are disabled.")

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        self.all_entities = all_entities
        return self.all_entities
