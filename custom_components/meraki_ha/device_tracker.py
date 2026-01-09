"""Support for Meraki client device tracking."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import (
    ScannerEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    CONF_FILTER_SSID,
    CONF_FILTER_VLAN,
    DOMAIN,
)
from .meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki device trackers from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    ssid_filter = entry.options.get(CONF_FILTER_SSID)
    vlan_filter = entry.options.get(CONF_FILTER_VLAN)

    @callback
    def async_update_scanners() -> None:
        """Update the list of device trackers."""
        if coordinator.data is None:
            return

        active_clients = {
            entity.unique_id for entity in hass.data[DOMAIN].get("entities", {}).get("device_tracker", [])
        }

        new_entities = []
        clients = coordinator.data.get("clients", {})
        for client_id, client in clients.items():
            if f"meraki-client-{client_id}" in active_clients:
                continue
            if vlan_filter and client.get("vlan") not in vlan_filter:
                continue
            if ssid_filter and client.get("ssid") not in ssid_filter:
                continue
            new_entities.append(
                MerakiClientTracker(hass, coordinator, entry, client)
            )

        async_add_entities(new_entities)

    entry.async_on_unload(coordinator.async_add_listener(async_update_scanners))
    async_update_scanners()


class MerakiClientTracker(
    CoordinatorEntity[MerakiDataCoordinator], ScannerEntity
):
    """Representation of a Meraki client."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        entry: ConfigEntry,
        client: dict[str, Any],
    ) -> None:
        """Initialize the client tracker."""
        super().__init__(coordinator)
        self.hass = hass
        self.config_entry = entry
        self._client_id = client["id"]
        self._attr_unique_id = f"meraki-client-{self._client_id}"
        self._attr_name = client.get("description") or client.get("mac")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self.name,
        }

    @property
    def is_connected(self) -> bool:
        """Return true if the client is connected to the network."""
        client = self._get_client()
        return client is not None and client.get("status") == "Online"

    @property
    def source_type(self) -> SourceType:
        """Return the source type, will be SourceType.ROUTER."""
        return SourceType.ROUTER

    @property
    def ip_address(self) -> str | None:
        """Return the primary ip address of the device."""
        client = self._get_client()
        return client.get("ip") if client else None

    @property
    def mac_address(self) -> str | None:
        """Return the mac address of the device."""
        client = self._get_client()
        return client.get("mac") if client else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the device state attributes."""
        client = self._get_client()
        if not client:
            return {}
        return {
            "vlan": client.get("vlan"),
            "ssid": client.get("ssid"),
            "status": client.get("status"),
        }

    def _get_client(self) -> dict[str, Any] | None:
        """Get the client data from the coordinator."""
        return self.coordinator.data.get("clients_by_id", {}).get(
            self._client_id
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
