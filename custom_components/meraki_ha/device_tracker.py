"""Support for Meraki client device tracking."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_FILTER_CLIENTS_SSID,
    CONF_FILTER_CLIENTS_VLAN,
    DOMAIN,
)
from .meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki device trackers from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    tracked_clients: dict[str, MerakiClientTracker] = {}

    @callback
    def _update_entities() -> None:
        """Update the tracked clients."""
        vlan_filter = [
            vlan.strip()
            for vlan in config_entry.options.get(CONF_FILTER_CLIENTS_VLAN, "").split(",")
            if vlan.strip()
        ]
        ssid_filter = [
            ssid.strip()
            for ssid in config_entry.options.get(CONF_FILTER_CLIENTS_SSID, "").split(",")
            if ssid.strip()
        ]

        new_tracked_clients: list[MerakiClientTracker] = []
        if coordinator.data and "clients" in coordinator.data:
            for client in coordinator.data["clients"]:
                if client["mac"] not in tracked_clients:
                    if (not vlan_filter or str(client.get("vlan")) in vlan_filter) and (
                        not ssid_filter or client.get("ssid") in ssid_filter
                    ):
                        tracker = MerakiClientTracker(coordinator, client)
                        tracked_clients[client["mac"]] = tracker
                        new_tracked_clients.append(tracker)

        if new_tracked_clients:
            async_add_entities(new_tracked_clients)

    config_entry.async_on_unload(coordinator.async_add_listener(_update_entities))
    _update_entities()


class MerakiClientTracker(CoordinatorEntity[MerakiDataCoordinator], TrackerEntity):
    """A Meraki client tracker."""

    _attr_translation_key = "presence"

    def __init__(self, coordinator: MerakiDataCoordinator, client_data: dict[str, Any]) -> None:
        """Initialize the tracker."""
        super().__init__(coordinator)
        self.client_data = client_data
        self._attr_unique_id = self.client_data["mac"]

    @property
    def is_connected(self) -> bool:
        """Return true if the client is connected."""
        return self.client_data["status"] == "Online"

    @property
    def source_type(self) -> SourceType:
        """Return the source type, will be SourceType.ROUTER."""
        return SourceType.ROUTER

    @property
    def ip_address(self) -> str | None:
        """Return the primary ip address of the device."""
        return self.client_data.get("ip")

    @property
    def mac_address(self) -> str:
        """Return the mac address of the device."""
        return self.client_data["mac"]

    @property
    def hostname(self) -> str | None:
        """Return hostname of the device."""
        return self.client_data.get("description")

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.mac_address)},
            name=self.hostname,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the client."""
        return {
            "ssid": self.client_data.get("ssid"),
            "vlan": self.client_data.get("vlan"),
            "ip": self.client_data.get("ip"),
            "last_seen": self.client_data.get("lastSeen"),
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if client_data := self.coordinator.clients_by_mac.get(self.unique_id):
            self.client_data = client_data
        else:
            self.client_data["status"] = "Offline"
        super()._handle_coordinator_update()
