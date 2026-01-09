"""Support for Meraki device tracking."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_FILTER_SSID,
    CONF_FILTER_VLAN,
    DATA_COORDINATOR,
    DOMAIN,
)
from .meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki device tracker platform."""
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    tracked: dict[str, MerakiClientDeviceTracker] = {}

    @callback
    def update_entities() -> None:
        """Update the device tracker entities."""
        if not coordinator.data or "clients" not in coordinator.data:
            _LOGGER.debug("No client data available from coordinator.")
            return

        new_entities = []

        filter_vlans = entry.options.get(CONF_FILTER_VLAN, [])
        filter_ssids = entry.options.get(CONF_FILTER_SSID, [])

        for client in coordinator.data["clients"]:
            if client["id"] in tracked:
                continue

            # Apply filters
            vlan = client.get("vlan")
            if filter_vlans and (vlan is None or vlan not in filter_vlans):
                continue

            ssid = client.get("ssid")
            if filter_ssids and (ssid is None or ssid not in filter_ssids):
                continue


            entity = MerakiClientDeviceTracker(coordinator, client)
            tracked[client["id"]] = entity
            new_entities.append(entity)

        if new_entities:
            async_add_entities(new_entities)

    entry.async_on_unload(coordinator.async_add_listener(update_entities))
    update_entities()


class MerakiClientDeviceTracker(CoordinatorEntity, ScannerEntity):
    """Representation of a tracked Meraki client."""

    _attr_translation_key = "presence"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the client tracker."""
        super().__init__(coordinator)
        self._client_id = client_data["id"]
        self._attr_unique_id = f"meraki_client_{self._client_id}"
        self._attr_name = (
            client_data.get("description") or client_data["mac"]
        )

    @property
    def is_connected(self) -> bool:
        """Return true if the client is connected to the network."""
        client = self._get_client_data()
        return client is not None and client.get("status") == "Online"

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the client."""
        return SourceType.ROUTER

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the client."""
        client = self._get_client_data()
        if not client:
            return {}

        return {
            "mac_address": client.get("mac"),
            "ip_address": client.get("ip"),
            "ssid": client.get("ssid"),
            "vlan": client.get("vlan"),
            "last_seen": client.get("lastSeen"),
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    def _get_client_data(self) -> dict[str, Any] | None:
        """Fetch the client's data from the coordinator."""
        return self.coordinator.clients_by_id.get(self._client_id)
