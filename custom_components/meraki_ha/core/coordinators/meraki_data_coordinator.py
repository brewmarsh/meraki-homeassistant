"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import (
    DOMAIN,
    CONF_IGNORED_NETWORKS,
    DEFAULT_IGNORED_NETWORKS,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    DEFAULT_HIDE_UNCONFIGURED_SSIDS,
)
from ...core.api.client import MerakiAPIClient as ApiClient

_LOGGER = logging.getLogger(__name__)


class MerakiDataCoordinator(DataUpdateCoordinator):
    """A centralized coordinator for Meraki API data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: ApiClient,
        scan_interval: int,
        config_entry: ConfigEntry,
    ) -> None:
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
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            # Filter ignored networks
            ignored_networks_str = self.config_entry.options.get(
                CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
            )
            if ignored_networks_str:
                ignored_names = {
                    name.strip() for name in ignored_networks_str.split(",")
                }
                if data.get("networks"):
                    data["networks"] = [
                        n
                        for n in data["networks"]
                        if n.get("name") not in ignored_names
                    ]

            # Filter unconfigured SSIDs
            if self.config_entry.options.get(
                CONF_HIDE_UNCONFIGURED_SSIDS, DEFAULT_HIDE_UNCONFIGURED_SSIDS
            ):
                if data.get("ssids"):
                    data["ssids"] = [
                        s for s in data["ssids"] if s.get("enabled") is True
                    ]

            return data
        except Exception as err:
            _LOGGER.error(
                "Unexpected error fetching Meraki data: %s", err, exc_info=True
            )
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_device(self, serial: str):
        """Get device data by serial number."""
        if self.data and self.data.get("devices"):
            for device in self.data["devices"]:
                if device.get("serial") == serial:
                    return device
        return None

    def get_network(self, network_id: str):
        """Get network data by ID."""
        if self.data and self.data.get("networks"):
            for network in self.data["networks"]:
                if network.get("id") == network_id:
                    return network
        return None

    def get_ssid(self, network_id: str, ssid_number: int):
        """Get SSID data by network ID and SSID number."""
        if self.data and self.data.get("ssids"):
            for ssid in self.data["ssids"]:
                if (
                    ssid.get("networkId") == network_id
                    and ssid.get("number") == ssid_number
                ):
                    return ssid
        return None
