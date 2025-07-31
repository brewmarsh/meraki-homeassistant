"""Coordinator for Meraki network data."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.helpers.update_coordinator import UpdateFailed

from .base import BaseMerakiCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkCoordinator(BaseMerakiCoordinator):
    """Coordinator to handle Meraki network data."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the network coordinator."""
        super().__init__(*args, **kwargs)
        self._networks: List[Dict[str, Any]] = []

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch network, client, and SSID data from Meraki.

        Returns:
            Dict containing network, client, and SSID data

        Raises:
            UpdateFailed: If update fails
        """
        try:
            networks = await self.api_client.get_networks()
            all_clients = []
            all_ssids = []
            processed_networks = []

            for network in networks:
                # Skip networks without required attributes
                if "id" not in network:
                    _LOGGER.warning("Network missing required attributes: %s", network)
                    continue
                network["productType"] = "network"

                # Fetch clients for this network
                try:
                    network_clients = await self.api_client.get_network_clients(
                        network["id"]
                    )
                    for client in network_clients:
                        client["networkId"] = network[
                            "id"
                        ]  # ensure networkId is present
                    all_clients.extend(network_clients)
                    network["client_count"] = len(network_clients)
                except Exception as err:
                    _LOGGER.warning(
                        "Error fetching client count for network %s: %s",
                        network.get("id"),
                        err,
                    )
                    network["client_count"] = 0

                # Fetch SSIDs if network supports wireless
                if 'wireless' in network.get("productTypes", []):
                    try:
                        network_ssids = await self.api_client.get_ssids(network["id"])
                        enabled_ssids = []
                        for ssid in network_ssids:
                            _LOGGER.debug("Processing SSID: %s", ssid)
                            if ssid.get("enabled"):
                                ssid["networkId"] = network["id"]
                                ssid["unique_id"] = f'{network["id"]}_{ssid["number"]}'
                                ssid["productType"] = "ssid"
                                enabled_ssids.append(ssid)
                        all_ssids.extend(enabled_ssids)
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching SSIDs for network %s: %s",
                            network.get("id"),
                            err,
                        )

                processed_networks.append(network)

            self._networks = processed_networks
            return {"networks": processed_networks, "clients": all_clients, "ssids": all_ssids}

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
