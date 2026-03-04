"""Migration and cleanup helpers for Meraki HA."""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# Patterns for old unique_ids
# 1. ssid-{network_id}-{ssid_number}-{switch_type}-switch
# 2. meraki-ssid-{network_id}-{ssid_number}-rf-profile
# 3. ssid-{network_id}-{ssid_number}-{attribute}
# 4. ssid-{network_id}-{ssid_number}_name_text
# 5. meraki-adult-content-filtering-{network_id}-{ssid_number}

RE_OLD_SSID_SWITCH = re.compile(r"^ssid-(.+)-(\d+)-(.+)-switch$")
RE_OLD_RF_PROFILE = re.compile(r"^meraki-ssid-(.+)-(\d+)-rf-profile$")
RE_OLD_SSID_SENSOR = re.compile(r"^ssid-(.+)-(\d+)-(.+)$")
RE_UNDERSCORE_SSID_SENSOR = re.compile(r"^([NL]_[0-9]+)_([0-9]+)_(.+)$")
RE_OLD_NAME_TEXT = re.compile(r"^ssid-(.+)-(\d+)_name_text$")
RE_OLD_ADULT_FILTER = re.compile(r"^meraki-adult-content-filtering-(.+)-(\d+)$")


def _get_new_unique_id(old_unique_id: str) -> str | None:
    """Map old unique IDs to the new standardized format."""
    # Check against patterns
    if match := RE_OLD_SSID_SWITCH.match(old_unique_id):
        net_id, ssid_num, sw_type = match.groups()
        return f"{net_id}ssid{ssid_num}_{sw_type}_switch"
    if match := RE_OLD_RF_PROFILE.match(old_unique_id):
        net_id, ssid_num = match.groups()
        return f"{net_id}ssid{ssid_num}_rf_profile"
    if match := RE_OLD_NAME_TEXT.match(old_unique_id):
        net_id, ssid_num = match.groups()
        return f"{net_id}ssid{ssid_num}_name_text"
    if match := RE_OLD_ADULT_FILTER.match(old_unique_id):
        net_id, ssid_num = match.groups()
        return f"{net_id}ssid{ssid_num}_adult_content_filtering"
    if match := RE_OLD_SSID_SENSOR.match(old_unique_id):
        net_id, ssid_num, attr = match.groups()
        # Avoid matching new format by accident
        if "ssid" not in net_id:
            return f"{net_id}ssid{ssid_num}_{attr}"
    if match := RE_UNDERSCORE_SSID_SENSOR.match(old_unique_id):
        net_id, ssid_num, attr = match.groups()
        # This handles the legacy N_123_0_walled_garden format
        return f"{net_id}ssid{ssid_num}_{attr}"
    return None


async def async_migrate_entities(hass: HomeAssistant, entry_id: str) -> None:
    """Migrate entity unique IDs to the new standardized format."""
    entity_registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(entity_registry, entry_id)

    for entity in entities:
        old_unique_id = entity.unique_id
        new_unique_id = _get_new_unique_id(old_unique_id)

        if new_unique_id and new_unique_id != old_unique_id:
            _LOGGER.info(
                "Migrating entity %s unique_id from %s to %s",
                entity.entity_id,
                old_unique_id,
                new_unique_id,
            )
            try:
                entity_registry.async_update_entity(
                    entity.entity_id, new_unique_id=new_unique_id
                )
            except ValueError as err:
                _LOGGER.error("Failed to migrate entity %s: %s", entity.entity_id, err)


async def async_cleanup_ghost_devices(hass: HomeAssistant, entry_id: str) -> None:
    """Remove old SSID devices.

    Note: [SSID] prefix is now canonical, so we no longer remove devices
    based on that prefix.
    """
    device_registry = dr.async_get(hass)
    devices = dr.async_entries_for_config_entry(device_registry, entry_id)

    for device in devices:
        should_remove = False

        # Check for old identifier format (DOMAIN, f"{network_id}:ssid:{ssid_number}")
        for identifier in device.identifiers:
            if identifier[0] == DOMAIN and ":ssid:" in identifier[1]:
                should_remove = True
                _LOGGER.info(
                    "Marking ghost device for removal (identifier match): %s",
                    identifier[1],
                )
                break

        if should_remove:
            # Only remove if it has no entities (or we just moved them)
            # Actually, if we migrated the entities' unique_ids, their device_info
            # will point to a NEW identifier, so they will be associated with a
            # new device when they next check in.
            # However, Home Assistant might still keep them linked to the old device
            # until the next refresh or if we explicitly move them.

            _LOGGER.info("Removing ghost device: %s", device.name or device.id)
            device_registry.async_remove_device(device.id)
