"""Device tracker platform for Meraki clients.

This module implements proper ScannerEntity-based device tracking for
Meraki network clients, following Home Assistant's device tracker entity
documentation.

When a Meraki client's MAC address matches an existing Home Assistant device
(e.g., Sonos, Apple TV), the tracker entity is added to that existing device
instead of creating a duplicate.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_CONNECTIONS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import (
    CONNECTION_NETWORK_MAC,
    DeviceInfo,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_ENABLE_DEVICE_TRACKER, DOMAIN
from .meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


def _find_existing_device_by_mac(
    hass: HomeAssistant,
    mac_address: str,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by MAC address.

    This allows us to link Meraki client tracking to existing devices
    like Sonos speakers, Apple TVs, smart TVs, etc.

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    mac_address : str
        The MAC address to search for (will be normalized).

    Returns
    -------
    dr.DeviceEntry | None
        The matching device entry, or None if not found.

    """
    # Normalize MAC address to lowercase with colons
    normalized_mac = mac_address.lower().replace("-", ":")

    try:
        device_registry = dr.async_get(hass)
    except (AttributeError, TypeError):
        return None

    # Search for device with matching MAC connection
    for device in device_registry.devices.values():
        if not device.connections:
            continue
        for conn_type, conn_id in device.connections:
            if conn_type == CONNECTION_NETWORK_MAC:
                # Normalize the stored MAC for comparison
                stored_mac = conn_id.lower().replace("-", ":")
                if stored_mac == normalized_mac:
                    _LOGGER.debug(
                        "Found existing device '%s' for MAC %s",
                        device.name,
                        mac_address,
                    )
                    return device
    return None


def _find_existing_device_by_ip(
    hass: HomeAssistant,
    ip_address: str,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by IP address.

    Many devices (IP cameras, smart TVs, network devices) use IP addresses
    as their primary identifier. This allows us to link Meraki client
    tracking to these devices.

    We check:
    1. Device configuration_url containing the IP
    2. Device identifiers containing the IP
    3. Entity unique_ids containing the IP

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    ip_address : str
        The IP address to search for.

    Returns
    -------
    dr.DeviceEntry | None
        The matching device entry, or None if not found.

    """
    if not ip_address:
        return None

    try:
        device_registry = dr.async_get(hass)
    except (AttributeError, TypeError):
        return None

    # Search devices by configuration_url or identifiers containing the IP
    for device in device_registry.devices.values():
        # Check configuration_url (many devices use http://IP:port)
        if device.configuration_url:
            # Check if IP is in the URL (handles http://192.168.1.1:8080 etc)
            if ip_address in device.configuration_url:
                # Skip our own Meraki devices
                if any(DOMAIN in str(ident) for ident in device.identifiers):
                    continue
                _LOGGER.debug(
                    "Found existing device '%s' for IP %s (via config_url)",
                    device.name,
                    ip_address,
                )
                return device

        # Check identifiers for IP address
        for identifier in device.identifiers:
            if len(identifier) >= 2:
                # identifier is (domain, id) - check if id contains IP
                if ip_address in str(identifier[1]):
                    # Skip our own Meraki devices
                    if identifier[0] == DOMAIN:
                        continue
                    _LOGGER.debug(
                        "Found existing device '%s' for IP %s (via identifier)",
                        device.name,
                        ip_address,
                    )
                    return device

    return None


def _find_existing_device(
    hass: HomeAssistant,
    mac_address: str | None,
    ip_address: str | None,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by MAC or IP address.

    Tries MAC first (most reliable), then falls back to IP.

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    mac_address : str | None
        The MAC address to search for.
    ip_address : str | None
        The IP address to search for.

    Returns
    -------
    dr.DeviceEntry | None
        The matching device entry, or None if not found.

    """
    # Try MAC address first (most reliable)
    if mac_address:
        device = _find_existing_device_by_mac(hass, mac_address)
        if device:
            return device

    # Fall back to IP address
    if ip_address:
        device = _find_existing_device_by_ip(hass, ip_address)
        if device:
            return device

    return None


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

        If a client's MAC matches an existing Home Assistant device (e.g.,
        Sonos, Apple TV), the tracker will be added to that device.
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
                        hass=hass,
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

    If the client's MAC matches an existing Home Assistant device (e.g.,
    Sonos, Apple TV, smart TV), the tracker entity is added to that
    existing device instead of creating a duplicate device entry.
    """

    _attr_has_entity_name = True
    _attr_device_info: DeviceInfo  # type: ignore[assignment]

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the device tracker.

        Parameters
        ----------
        hass : HomeAssistant
            The Home Assistant instance.
        coordinator : MerakiDataCoordinator
            The data update coordinator.
        config_entry : ConfigEntry
            The config entry for this integration.
        client_data : dict[str, Any]
            The client data from the Meraki API.

        """
        super().__init__(coordinator)
        self._hass = hass
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

        # Get client IP for device lookup
        client_ip = client_data.get("ip")

        # Check if this client matches an existing Home Assistant device
        # (e.g., Sonos speaker, Apple TV, smart TV, IP camera, etc.)
        # First tries MAC address, then falls back to IP address
        existing_device = _find_existing_device(hass, self._client_mac, client_ip)

        if existing_device:
            # Link to the existing device - add our entity to that device
            _LOGGER.info(
                "Linking Meraki client %s (IP: %s) to existing device '%s'",
                self._client_mac,
                client_ip,
                existing_device.name,
            )
            # Use the existing device's identifiers
            device_info = DeviceInfo(
                identifiers=existing_device.identifiers,
            )
            # Add MAC connection to help with future lookups
            device_info[ATTR_CONNECTIONS] = {(CONNECTION_NETWORK_MAC, self._client_mac)}
            self._linked_to_existing = True
        else:
            # Create a new client device under the Clients group
            # Hierarchy: Organization → Network → Clients Group → Client
            network_id = client_data.get("networkId")
            device_info = DeviceInfo(
                identifiers={(DOMAIN, f"client_{self._client_mac}")},
                name=self._attr_name,
                manufacturer=client_data.get("manufacturer"),
                connections={(CONNECTION_NETWORK_MAC, self._client_mac)},
            )
            # Link client to its Clients group (under network)
            if network_id:
                device_info["via_device"] = (
                    DOMAIN,
                    f"devicetype_{network_id}_clients",
                )
            self._linked_to_existing = False

        self._attr_device_info = device_info

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
