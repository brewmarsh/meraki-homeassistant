"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

from datetime import datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import (
    DOMAIN,
    CONF_IGNORED_NETWORKS,
    DEFAULT_IGNORED_NETWORKS,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    DEFAULT_HIDE_UNCONFIGURED_SSIDS,
    CONF_USE_STALE_DATA,
    CONF_STALE_DATA_THRESHOLD,
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
        self.devices_by_serial: dict = {}
        self.networks_by_id: dict = {}
        self.ssids_by_network_and_number: dict = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict = {}

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
            data = await self.api.get_all_data(self.last_successful_data)
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            self._filter_ignored_networks(data)
            self._filter_unconfigured_ssids(data)

            # Create lookup tables for efficient access in entities
            self.devices_by_serial = {
                d["serial"]: d for d in data.get("devices", []) if "serial" in d
            }
            self.networks_by_id = {
                n["id"]: n for n in data.get("networks", []) if "id" in n
            }
            self.ssids_by_network_and_number = {
                (s["networkId"], s["number"]): s
                for s in data.get("ssids", [])
                if "networkId" in s and "number" in s
            }

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
            self.last_successful_update = datetime.now()
            self.last_successful_data = data
            return data
        except Exception as err:
            use_stale = self.config_entry.options.get(CONF_USE_STALE_DATA, True)
            stale_threshold = self.config_entry.options.get(
                CONF_STALE_DATA_THRESHOLD, 30
            )
            if (
                use_stale
                and self.last_successful_update
                and (datetime.now() - self.last_successful_update)
                < timedelta(minutes=stale_threshold)
            ):
                _LOGGER.warning(
                    "Failed to fetch new Meraki data, using stale data from %s ago. Error: %s",
                    (datetime.now() - self.last_successful_update),
                    err,
                )
                return self.data

            _LOGGER.error(
                "Unexpected error fetching Meraki data: %s", err, exc_info=True
            )
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_device(self, serial: str):
        """Get device data by serial number."""
        return self.devices_by_serial.get(serial)

    def get_network(self, network_id: str):
        """Get network data by ID."""
        return self.networks_by_id.get(network_id)

    def get_ssid(self, network_id: str, ssid_number: int):
        """Get SSID data by network ID and SSID number."""
        return self.ssids_by_network_and_number.get((network_id, ssid_number))

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
