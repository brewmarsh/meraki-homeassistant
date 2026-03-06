"""Fetches client data for the Meraki coordinator."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice
    from ...core.models.network import MerakiNetwork
    from ..api import MerakiApiClientProtocol


_LOGGER = logging.getLogger(__name__)


class ClientFetcher:
    """Class to fetch client data."""

    def __init__(self, client: MerakiApiClientProtocol) -> None:
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
            self._client.run_with_semaphore(
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
            device.serial: self._client.run_with_semaphore(
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

    def derive_device_clients(
        self,
        network_clients: list[dict[str, Any]],
        devices: list[MerakiDevice],
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Derive device-level clients from network-level client data.

        This eliminates the need for multiple per-device API calls.

        Args:
            network_clients: A list of all clients in the organization's networks.
            devices: A list of devices to group clients for.

        Returns
        -------
            A dictionary of clients by device serial.
        """
        clients_by_serial: dict[str, list[dict[str, Any]]] = {}

        # Pre-initialize for requested devices to ensure keys exist
        for device in devices:
            if device.serial:
                clients_by_serial[device.serial] = []

        # Map clients to devices using recentDeviceSerial
        for client in network_clients:
            serial = client.get("recentDeviceSerial")
            if serial and serial in clients_by_serial:
                clients_by_serial[serial].append(client)

        _LOGGER.debug(
            "Derived device-level clients for %d devices from %d network clients",
            len(clients_by_serial),
            len(network_clients),
        )
        return clients_by_serial
