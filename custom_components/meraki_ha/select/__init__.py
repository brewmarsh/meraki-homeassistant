"""The select platform for the Meraki integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .meraki_content_filtering import MerakiContentFilteringSelect

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki select entities."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    ssid_firewall_coordinators = entry_data.get("ssid_firewall_coordinators", {})

    if coordinator.data and coordinator.data.get("ssids"):
        select_entities = []
        for ssid in coordinator.data["ssids"]:
            ssid_num = ssid.get("number")
            if not ssid.get("enabled") or ssid_num is None:
                continue

            firewall_coordinator = ssid_firewall_coordinators.get(ssid_num)
            if not firewall_coordinator:
                _LOGGER.warning(
                    "No firewall coordinator found for SSID %s", ssid_num
                )
                continue

            select_entities.append(
                MerakiContentFilteringSelect(
                    firewall_coordinator,
                    config_entry,
                    ssid,
                )
            )
        async_add_entities(select_entities)
