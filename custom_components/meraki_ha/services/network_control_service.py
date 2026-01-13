"""
Network Control Service.

This service is responsible for handling all network-level actions and data.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
<<<<<<< HEAD
<<<<<<< HEAD
    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.api.client import MerakiAPIClient
=======
<<<<<<< HEAD
    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.api.client import MerakiAPIClient
=======
    from ..core.api.client import MerakiAPIClient
    from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    from ..core.api.client import MerakiAPIClient
    from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


_LOGGER = logging.getLogger(__name__)


class NetworkControlService:
    """Service to control network-level settings."""

    def __init__(
        self,
        api_client: MerakiAPIClient,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
