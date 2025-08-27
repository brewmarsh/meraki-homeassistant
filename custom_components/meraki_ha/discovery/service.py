"""
Device Discovery Service

This module defines the DeviceDiscoveryService, which is responsible for
discovering devices from the Meraki data and delegating entity creation
to the appropriate handlers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .handlers.mr import MRHandler
from .handlers.mv import MVHandler
from .handlers.mx import MXHandler
from .handlers.gx import GXHandler
from .handlers.ms import MSHandler
from .handlers.mt import MTHandler
from .handlers.network import NetworkHandler
from .handlers.ssid import SSIDHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ..core.api.client import MerakiAPIClient
    from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ..core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ..services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


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
}


class DeviceDiscoveryService:
    """Service for discovering Meraki devices and creating corresponding entities."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
        meraki_client: "MerakiAPIClient",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._switch_port_coordinator = switch_port_coordinator
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service
        self._devices: List[MerakiDevice] = self._coordinator.data.get("devices", [])

    async def discover_entities(self) -> List["Entity"]:
        """
        Discover all entities for all devices and networks.

        This method iterates through all devices in the organization and uses
        the HANDLER_MAPPING to delegate entity creation to the appropriate
        handler based on the device's model type. It also discovers
        network-level and virtual SSID entities.
        """
        all_entities: List["Entity"] = []

        # Discover network-level entities
        network_handler = NetworkHandler(
            self._coordinator, self._config_entry, self._network_control_service
        )
        network_entities = await network_handler.discover_entities()
        all_entities.extend(network_entities)

        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

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
                )
            elif model_prefix in ("MX", "GX"):
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
                    self._switch_port_coordinator,
                    self._control_service,
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
        ssid_handler = SSIDHandler(
            self._coordinator, self._config_entry, self._meraki_client
        )
        ssid_entities = await ssid_handler.discover_entities()
        all_entities.extend(ssid_entities)

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
