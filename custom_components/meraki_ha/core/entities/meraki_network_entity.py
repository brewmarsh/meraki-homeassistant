"""Base entity for Meraki Networks."""

from __future__ import annotations

import logging

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...coordinators import MerakiMainCoordinator
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

        # Set has_entity_name to False to allow custom prefixed naming as requested
        # for network-level entities
        self._attr_has_entity_name = False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the network."""
        # The network is required for this entity, and so is its ID.
        network = self.network_data or self._network
        if network is None:
            raise ValueError("Network cannot be None")
        if network.id is None:
            raise ValueError("Network ID cannot be None")

        # Handle MerakiNetwork objects or raw dicts
        network_dict = network.to_dict() if hasattr(network, "to_dict") else network

        if info := resolve_device_info(network_dict, self.coordinator.config_entry):
            return info

        return DeviceInfo(
            identifiers={(DOMAIN, network.id)},
            name=standardize_device_name(network.name or f"Network {network.id}"),
            manufacturer="Cisco Meraki",
            model="Meraki Network",
        )
