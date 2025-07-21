"""Coordinator for Meraki network data."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.exceptions import UpdateFailed

from .base import BaseMerakiCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkCoordinator(BaseMerakiCoordinator):
    """Coordinator to handle Meraki network data."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the network coordinator."""
        super().__init__(*args, **kwargs)
        self._networks: List[Dict[str, Any]] = []

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch network data from Meraki.

        Returns:
            Dict containing network data

        Raises:
            UpdateFailed: If update fails
        """
        try:
            networks = await self.api_client.get_networks()
            processed_networks = []

            for network in networks:
                # Skip networks without required attributes
                if "id" not in network:
                    _LOGGER.warning("Network missing required attributes: %s", network)
                    continue

                # Fetch additional network data like client count
                try:
                    network["client_count"] = 0  # Placeholder for actual API call
                except Exception as err:
                    _LOGGER.warning(
                        "Error fetching client count for network %s: %s",
                        network.get("id"),
                        err,
                    )
                    network["client_count"] = 0

                processed_networks.append(network)

            self._networks = processed_networks
            return {"networks": processed_networks}

        except Exception as err:
            _LOGGER.error("Error fetching network data: %s", err)
            raise UpdateFailed(f"Error fetching network data: {err}")

    def get_network_by_id(self, network_id: str) -> Optional[Dict[str, Any]]:
        """Get a network by its ID.

        Args:
            network_id: Network ID

        Returns:
            Network data dictionary or None if not found
        """
        for network in self._networks:
            if network.get("id") == network_id:
                return network
        return None
