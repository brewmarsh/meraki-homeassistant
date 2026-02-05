"""Base entity for Meraki Networks."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.models.network import MerakiNetwork
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
    def device_info(self) -> DeviceInfo:
        """Return device info for the network."""
        # The network is required for this entity, and so is its ID.
        if self._network is None:
            raise ValueError("Network cannot be None")
        if self._network.id is None:
            raise ValueError("Network ID cannot be None")

        network_name = self._network.name or f"Network {self._network.id}"
        # Canonical Name Policy: [Network] Prefix
        if network_name and not str(network_name).startswith("[Network] "):
            network_name = f"[Network] {network_name}"

        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{self._network.id}")},
            name=str(network_name),
            manufacturer="Cisco Meraki",
            model="Meraki Network",
        )
