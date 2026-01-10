"""Device tracker platform for Meraki clients.

This module implements proper ScannerEntity-based device tracking for
Meraki network clients, following Home Assistant's device tracker entity
documentation.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_ENABLE_DEVICE_TRACKER, DOMAIN
from .meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up device tracker entities for Meraki clients.

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    config_entry : ConfigEntry
        The config entry for this integration.
    async_add_entities : AddEntitiesCallback
        Callback to add new entities.

    """
    if not config_entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
        _LOGGER.debug("Device tracker is disabled in options")
        return

    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: MerakiDataCoordinator = entry_data["coordinator"]

    # Track which clients we've already added
    tracked_clients: set[str] = set()

    @callback
    def async_add_client_trackers() -> None:
        """Add device trackers for new clients.

        Uses clients data from getNetworkClients() API which returns
        all clients connected to the network.
        """
        if not coordinator.data or not coordinator.data.get("clients"):
            return

        new_entities: list[MerakiClientDeviceTracker] = []

        for client_data in coordinator.data["clients"]:
            client_mac = client_data.get("mac")
            if not client_mac:
                continue

            if client_mac not in tracked_clients:
                tracked_clients.add(client_mac)
                new_entities.append(
                    MerakiClientDeviceTracker(
                        coordinator=coordinator,
                        config_entry=config_entry,
                        client_data=client_data,
                    )
                )

        if new_entities:
            _LOGGER.debug("Adding %d new client device trackers", len(new_entities))
            async_add_entities(new_entities)

    # Add initial clients
    async_add_client_trackers()

    # Register listener for future updates to add new clients
    config_entry.async_on_unload(
        coordinator.async_add_listener(async_add_client_trackers)
    )


class MerakiClientDeviceTracker(
    CoordinatorEntity,
    ScannerEntity,  # type: ignore[type-arg]
):
    """Representation of a Meraki client as a device tracker.

    This entity tracks the connection status of network clients using
    the ScannerEntity interface, which provides proper `home`/`not_home`
    states and integrates with Home Assistant's presence detection.
    """

    _attr_has_entity_name = True
    _attr_device_info: DeviceInfo  # type: ignore[assignment]

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the device tracker.

        Parameters
        ----------
        coordinator : MerakiDataCoordinator
            The data update coordinator.
        config_entry : ConfigEntry
            The config entry for this integration.
        client_data : dict[str, Any]
            The client data from the Meraki API.

        """
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._client_mac = client_data["mac"]
        self._attr_unique_id = f"meraki_client_{self._client_mac}"

        # Entity name - use description, hostname, or MAC
        self._attr_name = (
            client_data.get("description")
            or client_data.get("dhcpHostname")
            or client_data.get("ip")
            or self._client_mac
        )

        # Build device info - optionally link to parent device if known
        parent_serial = client_data.get("recentDeviceSerial")
        if parent_serial:
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, f"client_{self._client_mac}")},
                name=self._attr_name,
                manufacturer=client_data.get("manufacturer"),
                via_device=(DOMAIN, parent_serial),
            )
        else:
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, f"client_{self._client_mac}")},
                name=self._attr_name,
                manufacturer=client_data.get("manufacturer"),
            )

        # Cache client data for properties
        self._cached_client_data: dict[str, Any] = client_data

    @property
    def source_type(self) -> SourceType:
        """Return the source type (router).

        The Meraki integration monitors clients via the router/network
        infrastructure, so the source type is ROUTER.
        """
        return SourceType.ROUTER

    @property
    def is_connected(self) -> bool:
        """Return true if the client is currently connected.

        This property is required by ScannerEntity and determines whether
        the entity state is 'home' or 'not_home'.
        """
        if not self.coordinator.data or not self.coordinator.data.get("clients"):
            return False

        for client in self.coordinator.data["clients"]:
            if client.get("mac") == self._client_mac:
                # Update cached data when found
                self._cached_client_data = client
                # Presence in client list means connected
                return True

        return False

    @property
    def mac_address(self) -> str:
        """Return the MAC address of the device.

        This enables DHCP discovery integration for faster device detection.
        """
        return self._client_mac

    @property
    def ip_address(self) -> str | None:
        """Return the IP address of the device.

        This enables DHCP discovery integration.
        """
        return self._cached_client_data.get("ip")

    @property
    def hostname(self) -> str | None:
        """Return the hostname of the device.

        This enables DHCP discovery integration.
        """
        return self._cached_client_data.get(
            "dhcpHostname"
        ) or self._cached_client_data.get("description")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes.

        These provide extra context about the client that may be useful
        for automations or display.
        """
        attrs: dict[str, Any] = {}

        if self._cached_client_data:
            # Network connectivity info
            if ip6 := self._cached_client_data.get("ip6"):
                attrs["ip6_address"] = ip6
            if vlan := self._cached_client_data.get("vlan"):
                attrs["vlan"] = vlan
            if ssid := self._cached_client_data.get("ssid"):
                attrs["ssid"] = ssid
            if switchport := self._cached_client_data.get("switchport"):
                attrs["switchport"] = switchport

            # Connection type (wired vs wireless)
            if ssid:
                attrs["connection_type"] = "wireless"
            elif switchport:
                attrs["connection_type"] = "wired"

            # Client identification
            if manufacturer := self._cached_client_data.get("manufacturer"):
                attrs["manufacturer"] = manufacturer
            if os_type := self._cached_client_data.get("os"):
                attrs["os"] = os_type
            if user := self._cached_client_data.get("user"):
                attrs["user"] = user

            # Connection info - device the client is connected to
            if device_name := self._cached_client_data.get("recentDeviceName"):
                attrs["connected_to_device"] = device_name
            if device_serial := self._cached_client_data.get("recentDeviceSerial"):
                attrs["connected_to_serial"] = device_serial
            if device_mac := self._cached_client_data.get("recentDeviceMac"):
                attrs["connected_to_mac"] = device_mac

            # Group policy information
            if group_policy := self._cached_client_data.get("groupPolicy8021x"):
                attrs["group_policy"] = group_policy
            if policy_id := self._cached_client_data.get("policyId"):
                attrs["policy_id"] = policy_id

            # Timestamps
            if first_seen := self._cached_client_data.get("firstSeen"):
                attrs["first_seen"] = first_seen
            if last_seen := self._cached_client_data.get("lastSeen"):
                attrs["last_seen"] = last_seen

            # Usage stats
            if usage := self._cached_client_data.get("usage"):
                if isinstance(usage, dict):
                    attrs["sent_bytes"] = usage.get("sent", 0)
                    attrs["received_bytes"] = usage.get("recv", 0)

            # Additional network info
            if network_id := self._cached_client_data.get("networkId"):
                attrs["network_id"] = network_id

        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Update cached client data and trigger state update.
        """
        if self.coordinator.data and self.coordinator.data.get("clients"):
            for client in self.coordinator.data["clients"]:
                if client.get("mac") == self._client_mac:
                    self._cached_client_data = client
                    break

        self.async_write_ha_state()
