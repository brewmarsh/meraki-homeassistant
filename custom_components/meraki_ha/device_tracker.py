"""Platform for Meraki device tracker integration in Home Assistant."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .helpers.entity_helpers import format_entity_name


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki device tracker entities from a config entry."""
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    if not coordinator.data or "clients" not in coordinator.data:
        _LOGGER.warning("No client data available; cannot set up device trackers.")
        return

    clients: List[Dict[str, Any]] = coordinator.data.get("clients", [])
    if not clients:
        _LOGGER.info("No Meraki clients found to set up device trackers.")
        return

    entities = [
        MerakiDeviceTracker(coordinator, client_data)
        for client_data in clients
        if "mac" in client_data
    ]

    if entities:
        async_add_entities(entities)


class MerakiDeviceTracker(CoordinatorEntity[MerakiDataCoordinator], TrackerEntity):
    """Representation of an individual client device connected to a Meraki network."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        client_info: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki client device tracker."""
        super().__init__(coordinator)
        self._client_info_data = client_info
        name_format = self.coordinator.config_entry.options.get(
            "device_name_format", "prefix"
        )
        self._attr_name = format_entity_name(
            self._client_info_data.get("description")
            or self._client_info_data.get("ip"),
            "",
        )
        self._attr_unique_id = f"{self._client_info_data['mac']}_client_tracker"
        self._update_attributes()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attributes()
        self.async_write_ha_state()

    def _update_attributes(self) -> None:
        """Update entity attributes based on coordinator data."""
        self._attr_is_connected = False
        client_mac = self._client_info_data["mac"]

        if self.coordinator.data and "clients" in self.coordinator.data:
            for client_data in self.coordinator.data["clients"]:
                if client_data.get("mac") == client_mac:
                    self._attr_is_connected = True
                    self._client_info_data.update(client_data)
                    break

    @property
    def source_type(self) -> str:
        """Return the source type of the device tracker."""
        return SourceType.ROUTER

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information for linking this entity to the parent Meraki device."""
        parent_identifier_value = self._client_info_data.get(
            "ap_serial"
        ) or self._client_info_data.get("networkId", "meraki_network")
        return {"identifiers": {(DOMAIN, parent_identifier_value)}}

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lan-connect" if self.is_connected else "mdi:lan-disconnect"

    @property
    def is_connected(self) -> bool:
        """Return true if the device is connected to the network."""
        return self._attr_is_connected
