"""Fetches client data for the Meraki coordinator."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...types import MerakiDevice, MerakiNetwork
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class ClientFetcher:
    """Class to fetch client data."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """
        Initialize the client fetcher.

        Args:
            client: The Meraki API client.
        """
        self._client = client

    async def async_fetch_network_clients(
        self,
        networks: list[MerakiNetwork],
    ) -> list[dict[str, Any]]:
        """
        Fetch client data for all networks, used for SSID sensors.

        Args:
            networks: A list of networks to fetch clients for.

        Returns
        -------
            A list of clients.
        """
        client_tasks = [
            self._client._run_with_semaphore(
                self._client.network.get_network_clients(
                    network.id,
                    perPage=1000,
                    total_pages="all",
                ),
            )
            for network in networks
        ]
        clients_results = await asyncio.gather(*client_tasks, return_exceptions=True)
        clients: list[dict[str, Any]] = []
        for i, network in enumerate(networks):
            result = clients_results[i]
            if isinstance(result, list):
                _LOGGER.debug(
                    "Fetched %d clients for network %s", len(result), network.name
                )
                for client in result:
                    client["networkId"] = network.id
                clients.extend(result)
        return clients

    async def async_fetch_device_clients(
        self,
        devices: list[MerakiDevice],
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Fetch client data for each device.

        Args:
            devices: A list of devices to fetch clients for.

        Returns
        -------
            A dictionary of clients by device serial.
        """
        client_tasks = {
            device.serial: self._client._run_with_semaphore(
                self._client.devices.get_device_clients(device.serial),
            )
            for device in devices
            if device.serial
            and device.product_type
            in ("wireless", "appliance", "switch", "cellularGateway")
        }
        results = await asyncio.gather(*client_tasks.values(), return_exceptions=True)
        clients_by_serial: dict[str, list[dict[str, Any]]] = {}
        for i, serial in enumerate(client_tasks.keys()):
            result = results[i]
            if isinstance(result, list):
                clients_by_serial[serial] = result
        return clients_by_serial
