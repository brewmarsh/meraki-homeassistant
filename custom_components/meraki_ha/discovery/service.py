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


if TYPE_CHECKING:
    from ..hubs.organization import OrganizationHub
    from ...types import MerakiDevice
    from ..services.device_control_service import DeviceControlService
    from ..core.coordinators.switch_port_status_coordinator import SwitchPortStatusCoordinator


_LOGGER = logging.getLogger(__name__)

HANDLER_MAPPING = {
    "wireless": MRHandler,
    "appliance": MXHandler,
    "cellularGateway": GXHandler,
    "camera": MVHandler,
    "switch": MSHandler,
}


class DeviceDiscoveryService:
    """A service to discover devices and create corresponding entities."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
        control_service: "DeviceControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._control_service = control_service
        self._switch_port_coordinator = switch_port_coordinator
        self._devices: List[MerakiDevice] = self._coordinator.data.get("devices", [])

    def discover_entities(self) -> list:
        """
        Discover all entities for all devices.

        This method iterates through all devices in the organization and uses
        the HANDLER_MAPPING to delegate entity creation to the appropriate
        handler based on the device's product type.
        """
        all_entities = []
        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))
        for device in self._devices:
            product_type = device.get("productType")
            if not product_type:
                _LOGGER.warning("Device %s has no product type, skipping", device.get("serial"))
                continue

            handler_class = HANDLER_MAPPING.get(product_type)
            if not handler_class:
                _LOGGER.debug(
                    "No handler found for product type '%s', skipping device %s",
                    product_type,
                    device.get("serial"),
                )
                continue

            _LOGGER.debug(
                "Using handler %s for device %s",
                handler_class.__name__,
                device.get("serial"),
            )
            if product_type == "switch":
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                    self._switch_port_coordinator,
                )
            else:
                handler = handler_class(
                    self._coordinator,
                    device,
                    self._config_entry,
                    self._control_service,
                )
            discovered = handler.discover_entities()
            all_entities.extend(discovered)
            _LOGGER.debug(
                "Discovered %d entities for device %s",
                len(discovered),
                device.get("serial"),
            )

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
