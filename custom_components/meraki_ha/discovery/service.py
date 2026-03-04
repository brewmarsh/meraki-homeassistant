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
)
from ..core.models.device import MerakiDevice
from .handlers.network import NetworkHandler
from .handlers.switch import SwitchHandler
from .handlers.universal import UniversalHandler
from .handlers.wireless import WirelessHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ..coordinators import (
        MerakiApplianceCoordinator,
        MerakiCameraCoordinator,
        MerakiClientCoordinator,
        MerakiMainCoordinator,
        MerakiSensorCoordinator,
        MerakiSwitchCoordinator,
        MerakiWirelessCoordinator,
    )
    from ..core.api.client import MerakiAPIClient
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ..services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class DeviceDiscoveryService:
    """Service for discovering Meraki devices and creating corresponding entities."""

    def __init__(
        self,
        main_coordinator: MerakiMainCoordinator,
        switch_coordinator: MerakiSwitchCoordinator,
        camera_coordinator: MerakiCameraCoordinator,
        sensor_coordinator: MerakiSensorCoordinator,
        wireless_coordinator: MerakiWirelessCoordinator,
        appliance_coordinator: MerakiApplianceCoordinator,
        client_coordinator: MerakiClientCoordinator,
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._main_coordinator = main_coordinator
        self._switch_coordinator = switch_coordinator
        self._camera_coordinator = camera_coordinator
        self._sensor_coordinator = sensor_coordinator
        self._wireless_coordinator = wireless_coordinator
        self._appliance_coordinator = appliance_coordinator
        self._client_coordinator = client_coordinator

        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service

        devices_data = self._main_coordinator.data.get("devices", [])
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
        async for entity in self._discover_network_entities():
            all_entities.append(entity)

        # Discover device-level entities
        async for entity in self._discover_device_entities():
            all_entities.append(entity)

        # Create Wireless handler for devices and virtual SSID devices
        wireless_handler = WirelessHandler(
            self._wireless_coordinator, self._config_entry, self._meraki_client
        )
        async for entity in wireless_handler.discover_entities():
            all_entities.append(entity)

        # Create Switch handler for switch devices
        switch_handler = SwitchHandler(self._switch_coordinator, self._config_entry)
        async for entity in switch_handler.discover_entities():
            all_entities.append(entity)

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        self.all_entities = all_entities
        return self.all_entities

    async def _discover_network_entities(self):
        """Discover network-level entities."""
        if self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            network_handler = NetworkHandler(
                self._main_coordinator,
                self._config_entry,
                self._network_control_service,
            )
            async for entity in network_handler.discover_entities():
                yield entity
        else:
            _LOGGER.debug("Network sensors are disabled.")

    async def _discover_device_entities(self):
        """Discover entities for all devices."""
        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

        for device in self._devices:
            if not device.model:
                _LOGGER.warning("Device %s has no model, skipping", device.serial)
                continue

            coordinator = self._get_coordinator_for_device(device)

            handler = UniversalHandler(
                coordinator,
                device,
                self._config_entry,
                self._camera_service,
                self._control_service,
                self._network_control_service,
            )

            async for entity in handler.discover_entities():
                yield entity

    def _get_coordinator_for_device(self, device: MerakiDevice):
        """Select coordinator based on product type."""
        if device.product_type == "switch":
            return self._switch_coordinator
        if device.product_type == "camera":
            return self._camera_coordinator
        if device.product_type == "sensor":
            return self._sensor_coordinator
        if device.product_type in ["appliance", "cellularGateway"]:
            return self._appliance_coordinator
        if device.product_type == "wireless":
            return self._wireless_coordinator
        return self._main_coordinator
