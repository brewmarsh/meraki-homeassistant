"""Network Control Service.

This service is responsible for handling all network-level actions and data.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class NetworkControlService:
    """Service to control network-level settings."""

    def __init__(
        self,
        api_client: MerakiAPIClient,
        coordinator: MerakiDataUpdateCoordinator,
    ) -> None:
        """Initialize the network control service."""
        self._api_client = api_client
        self._coordinator = coordinator

    def get_network_client_count(self, network_id: str) -> int:
        """Get the number of clients on a specific network."""
        if not self._coordinator.data or not self._coordinator.data.get("clients"):
            return 0

        count = 0
        for client in self._coordinator.data["clients"]:
            if client.get("networkId") == network_id:
                count += 1
        return count
