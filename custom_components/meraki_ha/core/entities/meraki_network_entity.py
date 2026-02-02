"""Base entity for Meraki Networks."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo  # Ensure this is imported

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiNetwork
from . import BaseMerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkEntity(BaseMerakiEntity):
    """Representation of a Meraki Network."""

    coordinator: MerakiDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the network entity."""
        super().__init__(
            coordinator=coordinator, config_entry=config_entry, network_id=network.id
        )
        # CRITICAL: Keep this from 'beta' branch
        self._network = network

        # DEBUG: Keep this from 'fix' branch
        _LOGGER.debug(
            "Naming Debug - Entity: %s | Class: %s | has_entity_name: %s "
            "| _attr_name: %s | Device Identifiers: %s",
            self.entity_id if hasattr(self, "entity_id") else "New Entity",
            self.__class__.__name__,
            getattr(self, "_attr_has_entity_name", "Not Set"),
            getattr(self, "_attr_name", "None"),
            self.device_info.get("identifiers")
            if self.device_info
            else "NO DEVICE INFO",
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
