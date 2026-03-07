"""
Device Discovery Service.

This module defines the DeviceDiscoveryService, which is responsible for
discovering devices from the Meraki data and delegating entity creation
to the appropriate handlers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..const.config import (
    CONF_ENABLE_NETWORK_SENSORS,
)
from ..core.models.device import MerakiDevice
from homeassistant.exceptions import HomeAssistantError

from ..core.errors import MerakiHAException, MerakiInformationalError
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
        MerakiDeviceCoordinator,
        MerakiMainCoordinator,
        MerakiSensorCoordinator,
        MerakiSwitchCoordinator,
        MerakiWirelessCoordinator,
    )
    from ..core.api import MerakiApiClientProtocol
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ..services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class DeviceDiscoveryService:
    """Service for discovering Meraki devices and creating corresponding entities."""

    def __init__(
        self,
        main_coordinator: MerakiMainCoordinator,
        device_coordinator: MerakiDeviceCoordinator,
        switch_coordinator: MerakiSwitchCoordinator,
        camera_coordinator: MerakiCameraCoordinator,
        sensor_coordinator: MerakiSensorCoordinator,
        wireless_coordinator: MerakiWirelessCoordinator,
        appliance_coordinator: MerakiApplianceCoordinator,
        client_coordinator: MerakiClientCoordinator,
        config_entry: ConfigEntry,
        meraki_client: MerakiApiClientProtocol,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._main_coordinator = main_coordinator
        self._device_coordinator = device_coordinator
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

        self._devices: list[MerakiDevice] = list(
            self._device_coordinator.devices_by_serial.values()
        )
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
        try:
            async for entity in self._discover_network_entities():
                all_entities.append(entity)
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Failed to discover network entities: %s", e)

        # Discover device-level entities
        try:
            async for entity in self._discover_device_entities():
                all_entities.append(entity)
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Failed to discover device entities: %s", e)

        # Create Wireless handler for devices and virtual SSID devices
        try:
            wireless_handler = WirelessHandler(
                self._wireless_coordinator, self._config_entry, self._meraki_client
            )
            async for entity in wireless_handler.discover_entities():
                all_entities.append(entity)
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Failed to discover wireless entities: %s", e)

        # Create Switch handler for switch devices
        try:
            switch_handler = SwitchHandler(self._switch_coordinator, self._config_entry)
            async for entity in switch_handler.discover_entities():
                all_entities.append(entity)
        except (MerakiHAException, HomeAssistantError) as e:
            _LOGGER.error("Failed to discover switch entities: %s", e)

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
            try:
                async for entity in network_handler.discover_entities():
                    yield entity
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error("Error during network entity discovery: %s", e)
        else:
            _LOGGER.debug("Network sensors are disabled.")

    async def _discover_device_entities(self):
        """Discover entities for all devices."""
        # Refresh devices list from coordinator to ensure it's populated
        self._devices = list(self._device_coordinator.devices_by_serial.values())
        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

        for device in self._devices:
            if not device.model:
                _LOGGER.warning("Device %s has no model, skipping", device.serial)
                continue

            try:
                coordinator = self._get_coordinator_for_device(device)

                handler = UniversalHandler(
                    coordinator,
                    device,
                    self._config_entry,
                    self._camera_service,
                    self._control_service,
                    self._network_control_service,
                    status_coordinator=self._device_coordinator,
                    sensor_coordinator=self._sensor_coordinator,
                )

                async for entity in handler.discover_entities():
                    yield entity
            except (MerakiHAException, HomeAssistantError) as e:
                _LOGGER.error(
                    "Error discovering entities for device %s: %s", device.serial, e
                )
                continue

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
