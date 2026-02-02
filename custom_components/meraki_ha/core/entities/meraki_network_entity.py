"""Base entity for Meraki Networks."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry

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
        self._network = network
