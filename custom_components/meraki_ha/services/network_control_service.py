"""
Network Control Service.

This service is responsible for handling all network-level actions and data.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..coordinators import MerakiMainCoordinator
    from ..core.api import MerakiApiClientProtocol


_LOGGER = logging.getLogger(__name__)


class NetworkControlService:
    """Service to control network-level settings."""

    def __init__(
        self,
        api_client: MerakiApiClientProtocol,
        coordinator: MerakiMainCoordinator,
    ) -> None:
        """Initialize the network control service."""
        self._api_client = api_client
        self._coordinator = coordinator

    def get_network_client_count(self, network_id: str) -> int:
        """Get the number of clients on a specific network."""
        if not self._coordinator.data:
            return 0

        clients = self._coordinator.data.get("clients")

        # This safely handles both NoneType and unexpected dictionary/string returns
        if not isinstance(clients, list):
            return 0

        # Performance optimization: use generator expression with sum() instead of list
        # comprehension with len() to avoid allocating intermediate lists in memory.
        # This saves memory (O(1) vs O(N)) and provides a slight CPU boost.
        return sum(
            1
            for client in clients
            if isinstance(client, dict) and client.get("networkId") == network_id
        )
