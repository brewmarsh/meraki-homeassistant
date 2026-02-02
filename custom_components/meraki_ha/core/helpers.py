"""Standalone helper functions for the Meraki HA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..const import DOMAIN
from ..types import MerakiDevice, MerakiNetwork

if TYPE_CHECKING:
    from homeassistant.helpers.device_registry import DeviceRegistry
    from homeassistant.helpers.entity_registry import EntityRegistry


def update_device_registry_info(
    hass: HomeAssistant, devices: list[MerakiDevice]
) -> None:
    """Populate device data with associated Home Assistant entities.

    Args:
    ----
        hass: The Home Assistant instance.
        devices: The list of devices to populate.

    """
    if not devices:
        return

    ent_reg: EntityRegistry = er.async_get(hass)
    dev_reg: DeviceRegistry = dr.async_get(hass)

    for device in devices:
        device.status_messages = []
        if not device.serial:
            continue
        ha_device = dev_reg.async_get_device(
            identifiers={(DOMAIN, device.serial)},
        )
        if ha_device:
            entities_for_device = er.async_entries_for_device(
                ent_reg,
                ha_device.id,
            )
            if entities_for_device:
                # Prioritize camera entities, then switch, then fallback to first
                # This ensures the "navigate to entity" button on device page
                # goes to the most useful control entity.
                primary_entity = entities_for_device[0]
                for entity in entities_for_device:
                    if entity.domain == "camera":
                        primary_entity = entity
                        break
                    if entity.domain == "switch" and primary_entity.domain != "camera":
                        primary_entity = entity
                device.entity_id = primary_entity.entity_id


def filter_ignored_networks(data: dict[str, Any], ignored_ids: list[str]) -> None:
    """Filter out networks that the user has chosen to ignore.

    Args:
    ----
        data: The data dictionary to filter.
        ignored_ids: A list of network IDs to ignore.

    """
    if ignored_ids and "networks" in data:
        data["networks"] = [n for n in data["networks"] if n.id not in ignored_ids]


def process_coordinator_data(
    hass: HomeAssistant,
    config_entry: ConfigEntry | None,
    data: dict[str, Any],
) -> tuple[
    dict[str, MerakiDevice],
    dict[str, MerakiNetwork],
    dict[tuple[str, int], dict[str, Any]],
]:
    """Process raw API data into lookup tables and objects.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: The config entry.
        data: The raw data from the API (modified in place).

    Returns
    -------
        A tuple containing:
        - devices_by_serial
        - networks_by_id
        - ssids_by_network_and_number

    """
    # Create lookup tables for efficient access in entities
    devices_raw = data.get("devices", [])
    devices = [
        MerakiDevice.from_dict(d) if isinstance(d, dict) else d for d in devices_raw
    ]
    devices_by_serial = {d.serial: d for d in devices if d.serial}
    data["devices"] = devices

    networks_raw = data.get("networks", [])
    networks = [
        MerakiNetwork.from_dict(n) if isinstance(n, dict) else n for n in networks_raw
    ]
    networks_by_id = {n.id: n for n in networks if n.id}
    data["networks"] = networks

    # Pre-register network devices to avoid "referencing a non existing
    # via_device" warnings when downstream entities (like VLANs) initialize.
    device_registry = dr.async_get(hass)

    if config_entry:
        for network in networks:
            if not network.id:
                continue
            device_registry.async_get_or_create(
                config_entry_id=config_entry.entry_id,
                identifiers={(DOMAIN, cast(str, network.id))},
                name=network.name,
                manufacturer="Cisco Meraki",
                model="Network",
            )

    ssids_by_network_and_number = {
        (cast(str, s.get("networkId")), int(s.get("number"))): s
        for s in data.get("ssids", [])
        if s.get("networkId") and s.get("number") is not None
    }

    update_device_registry_info(hass, devices)

    return devices_by_serial, networks_by_id, ssids_by_network_and_number
