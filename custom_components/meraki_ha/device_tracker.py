"""Device tracker platform for Meraki clients.

This module implements proper ScannerEntity-based device tracking for
Meraki network clients, following Home Assistant's device tracker entity
documentation.

When a Meraki client's MAC or IP address matches an existing Home Assistant
device (e.g., Sonos, Apple TV), the tracker entity is added to that existing
device instead of creating a duplicate.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_ENABLE_DEVICE_TRACKER, DOMAIN
from .helpers.logging_helper import MerakiLoggers
from .meraki_data_coordinator import MerakiDataCoordinator

# Use feature-specific logger - can be configured independently via:
# logger:
#   logs:
#     custom_components.meraki_ha.device_tracker: warning
_LOGGER = MerakiLoggers.DEVICE_TRACKER


def _get_friendly_client_name(client_data: dict[str, Any]) -> str:
    """Generate a friendly name for a Meraki client.

    Priority order per requirements:
    1. Client description (from Dashboard) - e.g., "John's iPhone"
    2. DHCP hostname - e.g., "Johns-iPhone"
    3. Manufacturer + device type + last 4 MAC - e.g., "Apple iOS Device (ee:ff)"
    4. Manufacturer + last 4 MAC - e.g., "Apple Device (ee:ff)"
    5. MAC address (last resort only) - e.g., "aa:bb:cc:dd:ee:ff"

    Parameters
    ----------
    client_data : dict[str, Any]
        The client data from the Meraki API.

    Returns
    -------
    str
        A friendly, human-readable name for the client.

    """
    # Priority 1: Client description from Dashboard
    if description := client_data.get("description"):
        return description

    # Priority 2: DHCP hostname
    if hostname := client_data.get("dhcpHostname"):
        return hostname

    # Get MAC for fallback options (extract last 4 chars for uniqueness)
    mac = client_data.get("mac", "")
    last_4_mac = mac[-5:].replace(":", "") if len(mac) >= 5 else mac

    # Priority 3: Manufacturer + device type + last 4 MAC
    manufacturer = client_data.get("manufacturer")
    os_type = client_data.get("os")

    if manufacturer and os_type:
        return f"{manufacturer} {os_type} Device ({last_4_mac})"

    # Priority 4: Manufacturer + last 4 MAC
    if manufacturer:
        return f"{manufacturer} Device ({last_4_mac})"

    # Priority 5: MAC address (last resort)
    return mac


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
                    # Don't match our own Meraki client devices
                    if any(
                        DOMAIN in str(ident) and "client_" in str(ident)
                        for ident in device.identifiers
                    ):
                        continue
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

    Searches the entity registry for entities with matching IP addresses
    in their configuration, then returns the associated device.

    This helps match devices that don't expose MAC addresses but are
    configured with static IPs (e.g., some smart home devices).

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
        entity_registry = er.async_get(hass)
        device_registry = dr.async_get(hass)
    except (AttributeError, TypeError):
        return None

    # Search through entities that might have IP-based config
    # Common patterns: host, ip_address, address, ip in config
    for entity in entity_registry.entities.values():
        if not entity.device_id:
            continue

        # Check entity's config entry data for IP matches
        # This works for integrations that store IP in config
        if entity.config_entry_id:
            try:
                config_entry = hass.config_entries.async_get_entry(
                    entity.config_entry_id
                )
                if config_entry and config_entry.data:
                    # Check common IP field names in config
                    for key in ("host", "ip_address", "address", "ip"):
                        if config_entry.data.get(key) == ip_address:
                            device = device_registry.async_get(entity.device_id)
                            if device:
                                # Don't match our own Meraki client devices
                                if any(
                                    DOMAIN in str(ident) and "client_" in str(ident)
                                    for ident in device.identifiers
                                ):
                                    continue
                                _LOGGER.debug(
                                    "Found existing device '%s' for IP %s",
                                    device.name,
                                    ip_address,
                                )
                                return device
            except (AttributeError, KeyError):
                continue

    return None


def _find_existing_device(
    hass: HomeAssistant,
    mac_address: str,
    ip_address: str | None = None,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by MAC or IP address.

    Tries MAC first (more reliable), then falls back to IP matching.

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    mac_address : str
        The MAC address to search for.
    ip_address : str | None
        The IP address to search for (optional).

    Returns
    -------
    dr.DeviceEntry | None
        The matching device entry, or None if not found.

    """
    # Try MAC first - more reliable
    device = _find_existing_device_by_mac(hass, mac_address)
    if device:
        return device

    # Fall back to IP matching
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

        Filters out Meraki devices (APs, switches, etc.) that appear as
        "clients" on the network - we only want actual client devices.
        """
        if not coordinator.data or not coordinator.data.get("clients"):
            return

        # Build a set of Meraki device MACs to filter out
        # Meraki devices (APs, switches, sensors) appear as "clients" on the network
        # but we don't want to create device trackers for them
        meraki_device_macs: set[str] = set()
        for device in coordinator.data.get("devices", []):
            device_mac = device.get("mac")
            if device_mac:
                # Normalize to lowercase for comparison
                meraki_device_macs.add(device_mac.lower())

        new_entities: list[MerakiClientDeviceTracker] = []

        for client_data in coordinator.data["clients"]:
            client_mac = client_data.get("mac")
            if not client_mac:
                continue

            # Skip if this "client" is actually a Meraki device
            if client_mac.lower() in meraki_device_macs:
                _LOGGER.debug(
                    "Skipping client %s - it's a Meraki device, not a client",
                    client_mac,
                )
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
    Sonos, Apple TV), this entity is added to that device. Otherwise,
    a new client device is created.
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

        # Entity name - use friendly name per requirement priority:
        # 1. Client description (from Dashboard)
        # 2. DHCP hostname
        # 3. Manufacturer + device type + last 4 MAC
        # 4. Manufacturer + last 4 MAC
        # 5. MAC address (last resort only)
        self._attr_name = _get_friendly_client_name(client_data)

        # Get client IP for device lookup
        client_ip = client_data.get("ip")

        # Check if this client matches an existing Home Assistant device
        # (e.g., Sonos speaker, Apple TV, smart TV, etc.)
        # Try MAC first, then IP address for devices without exposed MACs
        client_ip = client_data.get("ip")
        existing_device = _find_existing_device(hass, self._client_mac, client_ip)

        if existing_device:
            # Link to the existing device - add our entity to that device
            _LOGGER.info(
                "Linking Meraki client %s to existing device '%s'",
                self._client_mac,
                existing_device.name,
            )
            # Use the existing device's identifiers to add our entity to it
            self._attr_device_info = DeviceInfo(
                identifiers=existing_device.identifiers,
            )
        else:
            # Create a new client device
            device_name = (
                client_data.get("description")
                or client_data.get("dhcpHostname")
                or client_data.get("ip")
                or self._client_mac
            )
            network_id = client_data.get("networkId")

            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, f"client_{self._client_mac}")},
                name=device_name,
                manufacturer=client_data.get("manufacturer") or "Unknown",
                connections={(CONNECTION_NETWORK_MAC, self._client_mac)},
            )

            # Link client to its network if available
            if network_id:
                self._attr_device_info["via_device"] = (DOMAIN, f"network_{network_id}")

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
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self._cached_client_data.get("latitude")

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self._cached_client_data.get("longitude")

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

            # Scanning API data
            if rssi := self._cached_client_data.get("rssi"):
                attrs["signal_strength"] = f"{rssi} dBm"

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
