"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import (
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_IGNORED_NETWORKS,
    DEFAULT_HIDE_UNCONFIGURED_SSIDS,
    DEFAULT_IGNORED_NETWORKS,
    DOMAIN,
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

    def _filter_ignored_networks(self, data: dict) -> None:
        """Filter out networks that the user has chosen to ignore."""
        ignored_networks_str = self.config_entry.options.get(
            CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
        )
        if ignored_networks_str and "networks" in data:
            ignored_names = {name.strip() for name in ignored_networks_str.split(",")}
            data["networks"] = [
                n for n in data["networks"] if n.get("name") not in ignored_names
            ]

    def _filter_unconfigured_ssids(self, data: dict) -> None:
        """Filter out unconfigured SSIDs if the user has chosen to hide them."""
        if (
            self.config_entry.options.get(
                CONF_HIDE_UNCONFIGURED_SSIDS, DEFAULT_HIDE_UNCONFIGURED_SSIDS
            )
            and "ssids" in data
        ):
            data["ssids"] = [s for s in data["ssids"] if s.get("enabled")]

    async def _async_update_data(self):
        """Fetch data from API endpoint and apply filters."""
        try:
            data = await self.api.get_all_data()
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            self._filter_ignored_networks(data)
            self._filter_unconfigured_ssids(data)

            if data and "devices" in data:
                ent_reg = er.async_get(self.hass)
                dev_reg = dr.async_get(self.hass)
                for device in data["devices"]:
                    if "status_messages" not in device:
                        device["status_messages"] = []

                    device["entities"] = []
                    ha_device = dev_reg.async_get_device(
                        identifiers={(DOMAIN, device["serial"])}
                    )
                    if ha_device:
                        entities_for_device = er.async_entries_for_device(
                            ent_reg, ha_device.id
                        )
                        for entity_entry in entities_for_device:
                            state = self.hass.states.get(entity_entry.entity_id)
                            if state:
                                device["entities"].append(
                                    {
                                        "entity_id": entity_entry.entity_id,
                                        "name": state.name,
                                        "state": state.state,
                                        "attributes": dict(state.attributes),
                                    }
                                )

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

    def add_status_message(self, serial: str, message: str) -> None:
        """Add a status message for a device."""
        if self.data and self.data.get("devices"):
            for device in self.data["devices"]:
                if device.get("serial") == serial:
                    if "status_messages" not in device:
                        device["status_messages"] = []
                    # Avoid duplicate messages
                    if message not in device["status_messages"]:
                        device["status_messages"].append(message)
                    break
