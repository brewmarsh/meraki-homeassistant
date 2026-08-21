"""Device tracker platform for Meraki clients."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const.integration import DOMAIN
from .coordinators import MerakiMainCoordinator
from .entity import MerakiDeviceTracker

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki device tracker platform."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return

    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovery_service = entry_data["discovery_service"]

    # Entities have already been discovered in __init__.py
    entities = []
    for entity in discovery_service.all_entities:
        if isinstance(entity, MerakiClientTracker):
            entities.append(entity)

    if entities:
        _LOGGER.debug("Adding %d Meraki device tracker entities", len(entities))
        async_add_entities(entities)


class MerakiClientTracker(MerakiDeviceTracker[MerakiMainCoordinator]):
    """Representation of a Meraki client as a device tracker."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        client_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the device tracker."""
        super().__init__(coordinator)
        self._client_mac: str = client_data["mac"]
        self._config_entry = config_entry

        client_name = (
            client_data.get("description") or client_data.get("ip") or self._client_mac
        )

        from homeassistant.helpers.device_registry import DeviceInfo

        from .core.utils.naming_utils import standardize_device_name

        device_info = DeviceInfo(
            identifiers={(DOMAIN, self._client_mac)},
            name=standardize_device_name(client_name),
            manufacturer=client_data.get("manufacturer", "Cisco Meraki"),
            model="Client",
        )

        if client_data.get("recentDeviceSerial"):
            device_info["via_device"] = (
                DOMAIN,
                str(client_data["recentDeviceSerial"]),
            )

        self._client_device_info = device_info

        self._attr_name = client_name
        self._attr_unique_id = f"{self._client_mac}_device_tracker"
        self._update_state(client_data)

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.ROUTER

    @property
    def mac_address(self) -> str:
        """Return the mac address of the device."""
        return self._client_mac

    @property
    def ip_address(self) -> str | None:
        """Return the primary ip address of the device."""
        attrs = self.extra_state_attributes or {}
        return attrs.get("ip_address")

    @property
    def hostname(self) -> str | None:
        """Return the hostname of the device."""
        attrs = self.extra_state_attributes or {}
        return attrs.get("description")

    def _get_current_client_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this client from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("clients"):
            for client in self.coordinator.data["clients"]:
                if not isinstance(client, dict):
                    continue
                if client.get("mac") == self._client_mac:
                    return client
        return None

    @property
    def is_connected(self) -> bool:
        """Return true if the device is connected to the network."""
        attrs = self.extra_state_attributes or {}
        return attrs.get("status") == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self, client_data: dict[str, Any] | None = None) -> None:
        """Update state from coordinator data."""
        current_client_data = client_data or self._get_current_client_data()
        if not current_client_data:
            self._attr_extra_state_attributes = {"status": "offline"}
            return

        status = current_client_data.get("status", "Offline")
        self._attr_extra_state_attributes = {
            "status": status.lower(),
            "mac_address": current_client_data.get("mac"),
            "ip_address": current_client_data.get("ip"),
            "description": current_client_data.get("description"),
            "ssid": current_client_data.get("ssid"),
            "vlan": current_client_data.get("vlan"),
            "os": current_client_data.get("os"),
            "manufacturer": current_client_data.get("manufacturer"),
            "recent_device_serial": current_client_data.get("recentDeviceSerial"),
        }
