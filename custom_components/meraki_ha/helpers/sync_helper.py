"""Helpers for bidirectional data synchronization."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


def find_root_device(
    device_registry: dr.DeviceRegistry,
    device: dr.DeviceEntry,
) -> dr.DeviceEntry:
    """Find the root/parent device in a hierarchy.

    Traverses up the device hierarchy (via via_device_id) to find the
    root device. This is useful for getting a meaningful name for
    child devices (e.g., getting "SunPower Gateway" for a panel).

    Args:
    ----
        device_registry: The device registry.
        device: The device to find the root for.

    Returns
    -------
        The root device in the hierarchy.

    """
    current = device
    visited = set()  # Prevent infinite loops

    while current.via_device_id and current.id not in visited:
        visited.add(current.id)
        parent = device_registry.async_get(current.via_device_id)
        if parent:
            current = parent
        else:
            break
    return current


def build_client_description(
    hass: HomeAssistant,
    client_mac: str,
    include_model: bool = True,
    include_version: bool = False,
    config_entry: ConfigEntry | None = None,
) -> str | None:
    """Build a description from a Home Assistant device.

    This finds the HA device matching the MAC address, traverses to its
    root device, and builds a description string that can be synced to
    Meraki Dashboard.

    Args:
    ----
        hass: The Home Assistant instance.
        client_mac: The MAC address of the client.
        include_model: Whether to include the device model in the description.
        include_version: Whether to include the SW version in the description.
        config_entry: Optional config entry to read options from.

    Returns
    -------
        A description string, or None if no matching device found.

    """
    # If config_entry provided, read options from it
    if config_entry:
        from ..const import (
            CONF_SYNC_INCLUDE_MODEL,
            CONF_SYNC_INCLUDE_VERSION,
            DEFAULT_SYNC_INCLUDE_MODEL,
            DEFAULT_SYNC_INCLUDE_VERSION,
        )

        include_model = config_entry.options.get(
            CONF_SYNC_INCLUDE_MODEL, DEFAULT_SYNC_INCLUDE_MODEL
        )
        include_version = config_entry.options.get(
            CONF_SYNC_INCLUDE_VERSION, DEFAULT_SYNC_INCLUDE_VERSION
        )

    device_registry = dr.async_get(hass)
    ha_device = None
    for device in device_registry.devices.values():
        for conn_type, conn_id in device.connections:
            if (
                conn_type == CONNECTION_NETWORK_MAC
                and conn_id.lower() == client_mac.lower()
            ):
                ha_device = device
                break
        if ha_device:
            break

    if not ha_device:
        return None

    root_device = find_root_device(device_registry, ha_device)
    parts = []

    # Always include the device name
    if root_device.name:
        parts.append(root_device.name)

    # Optionally include model
    if include_model and root_device.model:
        parts.append(f"({root_device.model})")

    # Optionally include software version
    if include_version and root_device.sw_version:
        parts.append(f"[{root_device.sw_version}]")

    return " ".join(parts) if parts else None


def get_sync_candidates(
    hass: HomeAssistant,
    clients: list[dict[str, Any]],
    config_entry: ConfigEntry | None = None,
) -> list[dict[str, Any]]:
    """Get a list of clients that can be synced to Meraki.

    Compares current Meraki client descriptions with HA device names
    and returns clients where the name would change.

    Args:
    ----
        hass: The Home Assistant instance.
        clients: List of client data from Meraki coordinator.
        config_entry: Optional config entry to read options from.

    Returns
    -------
        List of dicts with mac, name, networkId for clients to update.

    """
    candidates = []

    for client in clients:
        mac = client.get("mac")
        if not mac:
            continue

        current_description = client.get("description") or ""
        new_description = build_client_description(hass, mac, config_entry=config_entry)

        if new_description and new_description != current_description:
            candidates.append(
                {
                    "mac": mac,
                    "name": new_description,
                    "networkId": client.get("networkId"),
                    "current_name": current_description,
                }
            )

    return candidates
