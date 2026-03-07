"""Base entity for Meraki Networks."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from custom_components.meraki_ha.const.integration import DOMAIN

from...coordinators import MerakiMainCoordinator
from ...core.models.network import MerakiNetwork
from ...core.utils.naming_utils import standardize_device_name
from ...helpers.device_info_helpers import resolve_device_info
from . import BaseMerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkEntity(BaseMerakiEntity):
    """Representation of a Meraki Network."""

    coordinator: MerakiMainCoordinator

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
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

        if info := resolve_device_info(
            self._network.to_dict(), self.coordinator.config_entry
        ):
            return info

        return DeviceInfo(
            identifiers={(DOMAIN, self._network.id)},
            name=standardize_device_name(
                self._network.name or f"Network {self._network.id}"
            ),
            manufacturer="Cisco Meraki",
            model="Meraki Network",
        )
