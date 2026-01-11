"""
Network Control Service.

This service is responsible for handling all network-level actions and data.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..core.api.client import MerakiAPIClient
    from ..meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = MerakiLoggers.MAIN


class NetworkControlService:
    """Service to control network-level settings."""

    def __init__(
        self,
        api_client: MerakiAPIClient,
        coordinator: MerakiDataCoordinator,
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
