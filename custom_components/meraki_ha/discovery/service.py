"""
Device Discovery Service.

This module defines the DeviceDiscoveryService, which is responsible for
discovering devices from the Meraki data and delegating entity creation
to the appropriate handlers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..const import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
)
from .handlers.cs import CSHandler
from .handlers.cw import CWHandler
from .handlers.gx import GXHandler
from .handlers.mg import MGHandler
from .handlers.mr import MRHandler
from .handlers.ms import MSHandler
from .handlers.mt import MTHandler
from .handlers.mv import MVHandler
from .handlers.mx import MXHandler
from .handlers.network import NetworkHandler
from .handlers.ssid import SSIDHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...types import MerakiDevice
    from ..core.api.client import MerakiAPIClient
    from ..meraki_data_coordinator import MerakiDataCoordinator
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ..services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)

HANDLER_MAPPING = {
    "MR": MRHandler,
    "MV": MVHandler,
    "MX": MXHandler,
    "GX": GXHandler,
    "MS": MSHandler,
    "GS": MSHandler,
    "MT": MTHandler,
    "GR": GXHandler,
    "MG": MGHandler,  # Cellular Gateway
    "CW": CWHandler,  # Catalyst Wireless
    "C9": CSHandler,  # Catalyst Switch (C9xxx models)
}


class DeviceDiscoveryService:
    """Service for discovering Meraki devices and creating corresponding entities."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
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
        self._devices: list[MerakiDevice] = self._coordinator.data.get("devices", [])

    async def discover_entities(self) -> list[Entity]:
        """
        Discover all entities for all devices and networks.

        This method iterates through all devices in the organization and uses
        the HANDLER_MAPPING to delegate entity creation to the appropriate
        handler based on the device's model type. It also discovers
        network-level and virtual SSID entities.
        """
        all_entities: list[Entity] = []

        # Discover network-level entities
        if self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            network_handler = NetworkHandler.create(
                self._coordinator,
                None,
                self._config_entry,
                self._camera_service,
                self._control_service,
                self._network_control_service,
            )
            network_entities = await network_handler.discover_entities()
            all_entities.extend(network_entities)
        else:
            _LOGGER.debug("Network sensors are disabled.")

        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

        # Check global device entity processing
        process_devices = self._config_entry.options.get(
            CONF_ENABLE_DEVICE_STATUS, True
        )

        if not process_devices:
            _LOGGER.debug("Device processing (Device & Entity Model) is disabled.")

        for device in self._devices:
            model = device.get("model")
            if not model:
                _LOGGER.warning(
                    "Device %s has no model, skipping", device.get("serial")
                )
                continue

            # Get the first two letters of the model (e.g., "MR" from "MR36")
            model_prefix = model[:2]
            handler_class = HANDLER_MAPPING.get(model_prefix)

            if not handler_class:
                _LOGGER.debug(
                    "No handler found for model '%s', skipping device %s",
                    model,
                    device.get("serial"),
                )
                continue

            # Check configuration options before creating handlers

            # If basic device processing is disabled, we might still want to process
            # specialized sensors if they are enabled separately (e.g. cameras),
            # but typically "Device & Entity Model" implies the core device
            # representation. However, Home Assistant entities need a device
            # association. If we disable "Device & Entity Model", we probably
            # shouldn't create *any* entities for the device, unless a specific
            # override exists. For now, if process_devices is False, we skip
            # unless it is a specialized type that has its own toggle which is ON.

            # Actually, the simplest interpretation is:
            # CONF_ENABLE_DEVICE_STATUS -> generic device entities (like reboot
            # button, status sensors)
            # CONF_ENABLE_CAMERA_ENTITIES -> camera entities
            # CONF_ENABLE_DEVICE_SENSORS -> MT sensors

            # But handlers create multiple things.
            # I will pass the config down or decide here.

            # Special case for cameras:
            if model_prefix == "MV":
                if not self._config_entry.options.get(
                    CONF_ENABLE_CAMERA_ENTITIES, True
                ):
                    _LOGGER.debug(
                        "Camera entities are disabled, skipping device %s",
                        device.get("serial"),
                    )
                    continue

            # Special case for MT sensors:
            elif model_prefix == "MT":
                if not self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
                    _LOGGER.debug(
                        "Device sensors are disabled, skipping device %s",
                        device.get("serial"),
                    )
                    continue

            # For other devices (MR, MS, MX, GX), if generic device status is disabled,
            # we check if they have other enabled features.
            # MS has Port Sensors.
            # MX/GX has Port Sensors (uplinks).
            # MR doesn't have specific toggle other than Network/SSID which are
            # separate.

            elif not process_devices:
                # Check exceptions for devices with sub-features that are enabled
                has_enabled_features = False
                if model_prefix in (
                    "MS",
                    "MX",
                    "GX",
                ) and self._config_entry.options.get("enable_port_sensors", True):
                    has_enabled_features = True

                if not has_enabled_features:
                    continue

            _LOGGER.debug(
                "Using handler %s for device %s",
                handler_class.__name__,
                device.get("serial"),
            )

            # Pass the correct services to the handler based on its type
            if model_prefix == "MV":
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._camera_service,
                    self._control_service,
                    self._network_control_service,
                    self._meraki_client,
                )
            elif model_prefix in ("MX", "GX", "GR"):
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                    self._network_control_service,
                )
            elif model_prefix in ("MS", "GS"):
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                    self._network_control_service,
                )
            elif model_prefix == "MR":
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                    self._network_control_service,
                )
            else:
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                )

            entities = await handler.discover_entities()
            all_entities.extend(entities)

        # Create SSID handler for virtual SSID devices
        if self._config_entry.options.get(CONF_ENABLE_SSID_SENSORS, True):
            ssid_handler = SSIDHandler.create(
                self._coordinator, self._config_entry, self._meraki_client
            )
            ssid_entities = await ssid_handler.discover_entities()
            all_entities.extend(ssid_entities)
        else:
            _LOGGER.debug("SSID sensors are disabled.")

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
