"""Coordinator for SSID firewall rules and client policies."""

from __future__ import annotations

import logging
from typing import Any

from ...coordinators.base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class SsidFirewallCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for SSID firewall rules and client policies."""

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Meraki API."""
        clients_data = []
        for network_id in self.networks_by_id:
            try:
                # Fetch clients for the last 24 hours to get a good sample
                # Meraki API returns policy in this list
                clients = await self.api.network.get_network_clients(
                    network_id=network_id,
                    timespan=86400,
                )
                clients_data.extend(clients)
            except Exception as err:
                _LOGGER.error(
                    "Error fetching clients for network %s: %s", network_id, err
                )

        return {
            "rules": [],
            "clients": clients_data,
        }

    async def async_block_client(self, client_mac: str, network_id: str) -> None:
        """Block a client using MAC-based policy."""
        _LOGGER.debug("Blocking client %s in network %s", client_mac, network_id)
        try:
            await self.api.network.update_network_client_policy(
                network_id=network_id,
                client_mac=client_mac,
                device_policy="Blocked",
            )
            self.register_pending_update(f"client_blocker_{client_mac}")
            # Request refresh to update state in HA
            await self.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error blocking client %s: %s", client_mac, err)
            raise

    async def async_unblock_client(self, client_mac: str, network_id: str) -> None:
        """Unblock a client using MAC-based policy."""
        _LOGGER.debug("Unblocking client %s in network %s", client_mac, network_id)
        try:
            await self.api.network.update_network_client_policy(
                network_id=network_id,
                client_mac=client_mac,
                device_policy="Normal",
            )
            self.register_pending_update(f"client_blocker_{client_mac}")
            # Request refresh to update state in HA
            await self.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error unblocking client %s: %s", client_mac, err)
            raise
