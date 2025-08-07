"""Data update coordinator for the Meraki HA integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import DOMAIN
from ...core.api.client import MerakiAPIClient as ApiClient

_LOGGER = logging.getLogger(__name__)


class MerakiDataCoordinator(DataUpdateCoordinator):
    """A centralized coordinator for Meraki API data."""

    def __init__(self, hass, api_client: ApiClient, scan_interval: int, config_entry):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api_client
        self.config_entry = config_entry

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to fetch data from the API and return it.
        """
        try:
            data = await self.api.get_all_data()

            # Process clients to count them per device
            client_counts = {}
            clients = data.get("clients", [])
            _LOGGER.debug(f"Found {len(clients)} total clients")
            if clients:
                _LOGGER.debug(f"First client data: {clients[0]}")
            for client in clients:
                if client.get("status") == "Online":
                    serial = client.get("recentDeviceSerial")
                    if serial:
                        client_counts[serial] = client_counts.get(serial, 0) + 1
            _LOGGER.debug(f"Final client counts: {client_counts}")

            # Add client count to each device
            devices = data.get("devices", [])
            for device in devices:
                device["connected_clients_count"] = client_counts.get(
                    device["serial"], 0
                )

            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_device(self, serial: str):
        """Get device data by serial number."""
        if self.data and self.data.get("devices"):
            for device in self.data["devices"]:
                if device.get("serial") == serial:
                    return device
        return None
