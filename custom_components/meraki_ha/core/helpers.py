"""Standalone helper functions for the Meraki HA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..const import DOMAIN
from ..types import MerakiDevice

if TYPE_CHECKING:
    from homeassistant.helpers.device_registry import DeviceRegistry
    from homeassistant.helpers.entity_registry import EntityRegistry


def update_device_registry_info(
    hass: HomeAssistant, devices: list[MerakiDevice]
) -> None:
    """Populate device data with associated Home Assistant entities.

    Args:
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
        data: The data dictionary to filter.
        ignored_ids: A list of network IDs to ignore.
    """
    if ignored_ids and "networks" in data:
        data["networks"] = [n for n in data["networks"] if n.id not in ignored_ids]
