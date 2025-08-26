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

if TYPE_CHECKING:
    from ..hubs.organization import OrganizationHub
    from ...types import MerakiDevice
    # from .handlers.ms import MSHandler
    # from .handlers.mx import MXHandler
    # from .handlers.mv import MVHandler

_LOGGER = logging.getLogger(__name__)
# In the future, this will be a mapping of product types to handler classes
# from .handlers.ms import MSHandler
# from .handlers.mx import MXHandler
# from .handlers.mv import MVHandler
HANDLER_MAPPING = {
    "wireless": MRHandler,
    # "switch": MSHandler,
    # "appliance": MXHandler,
    # "camera": MVHandler,
}


class DeviceDiscoveryService:
    """A service to discover devices and create corresponding entities."""

    def __init__(self, org_hub: OrganizationHub) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._org_hub = org_hub
        self._devices: List[MerakiDevice] = self._org_hub.data.get("devices", [])

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
            handler = handler_class(device)
            discovered = handler.discover_entities()
            all_entities.extend(discovered)
            _LOGGER.debug(
                "Discovered %d entities for device %s",
                len(discovered),
                device.get("serial"),
            )

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
