"""Base class for Meraki client sensor entities.

This module provides the base class for all client sensor entities,
handling device linking (to existing HA devices or new client devices)
and coordinator updates.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...helpers.logging_helper import MerakiLoggers
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.DEVICE_TRACKER


def _find_existing_device_by_mac(
    hass: HomeAssistant,
    mac_address: str,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by MAC address.

    This allows us to link Meraki client sensors to existing devices
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
                    return device
    return None


def _find_existing_device_by_ip(
    hass: HomeAssistant,
    ip_address: str,
) -> dr.DeviceEntry | None:
    """Find an existing Home Assistant device by IP address.

    Searches the entity registry for entities with matching IP addresses
    in their configuration, then returns the associated device.

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
    for entity in entity_registry.entities.values():
        if not entity.device_id:
            continue

        if entity.config_entry_id:
            try:
                config_entry = hass.config_entries.async_get_entry(
                    entity.config_entry_id
                )
                if config_entry and config_entry.data:
                    for key in ("host", "ip_address", "address", "ip"):
                        if config_entry.data.get(key) == ip_address:
                            device = device_registry.async_get(entity.device_id)
                            if device:
                                if any(
                                    DOMAIN in str(ident) and "client_" in str(ident)
                                    for ident in device.identifiers
                                ):
                                    continue
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
    device = _find_existing_device_by_mac(hass, mac_address)
    if device:
        return device

    if ip_address:
        device = _find_existing_device_by_ip(hass, ip_address)
        if device:
            return device

    return None


class MerakiClientSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Meraki client sensor entities.

    Provides common functionality for linking sensors to the appropriate
    device (existing HA device or new Meraki client device) and updating
    from coordinator data.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
        sensor_key: str,
    ) -> None:
        """Initialize the client sensor.

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
        sensor_key : str
            The unique key for this sensor type (e.g., "vlan", "ssid").

        """
        super().__init__(coordinator)
        self._hass = hass
        self._config_entry = config_entry
        self._client_mac = client_data["mac"]
        self._attr_unique_id = f"meraki_client_{self._client_mac}_{sensor_key}"

        # Check if this client matches an existing Home Assistant device
        # Try MAC first, then IP address for devices without exposed MACs
        client_ip = client_data.get("ip")
        existing_device = _find_existing_device(hass, self._client_mac, client_ip)

        if existing_device:
            # Link to the existing device
            self._attr_device_info = DeviceInfo(
                identifiers=existing_device.identifiers,
            )
        else:
            # Link to the Meraki client device (created by device_tracker)
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

            if network_id:
                self._attr_device_info["via_device"] = (DOMAIN, f"network_{network_id}")

        # Cache client data
        self._cached_client_data: dict[str, Any] = client_data

    @property
    @abstractmethod
    def native_value(self) -> Any:
        """Return the sensor value. Must be implemented by subclasses."""

    def _get_current_client_data(self) -> dict[str, Any] | None:
        """Get the current client data from the coordinator.

        Returns
        -------
        dict[str, Any] | None
            The current client data, or None if not found.

        """
        if not self.coordinator.data or not self.coordinator.data.get("clients"):
            return None

        for client in self.coordinator.data["clients"]:
            if client.get("mac") == self._client_mac:
                return client

        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        client_data = self._get_current_client_data()
        if client_data:
            self._cached_client_data = client_data

        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if the client is currently connected."""
        return self._get_current_client_data() is not None
