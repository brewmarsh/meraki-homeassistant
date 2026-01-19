"""
Network Control Service.

This service is responsible for handling all network-level actions and data.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
<<<<<<< HEAD
    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.api.client import MerakiAPIClient
=======
    from ..core.api.client import MerakiAPIClient
    from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)


_LOGGER = logging.getLogger(__name__)


class NetworkControlService:
    """Service to control network-level settings."""

    def __init__(
        self,
        api_client: MerakiAPIClient,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
    ) -> None:
        """Initialize the network control service."""
        self._api_client = api_client
        self._coordinator = coordinator

    def get_network_client_count(self, network_id: str) -> int:
        """Get the number of clients on a specific network."""
        if not self._coordinator.data or not self._coordinator.data.get("clients"):
            return 0

<<<<<<< HEAD
        return len(
            [
                client
                for client in self._coordinator.data["clients"]
                if client.get("networkId") == network_id
            ]
        )
=======
        count = 0
        for client in self._coordinator.data["clients"]:
            if client.get("networkId") == network_id:
                count += 1
        return count
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
