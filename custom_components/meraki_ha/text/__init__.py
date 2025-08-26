"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.text import TextEntity

from ..const import (
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Add discovered entities
    discovered_entities = entry_data.get("entities", [])

    text_entities = [e for e in discovered_entities if isinstance(e, TextEntity)]

    # The other text entities are not created by the discovery service, so we need to create them here
    coordinator = entry_data["coordinator"]
    meraki_client = entry_data["client"]

    if coordinator and coordinator.data and "ssids" in coordinator.data:
        ssids = coordinator.data["ssids"]
        for ssid_data in ssids:
            if not isinstance(ssid_data, dict):
                continue
            network_id = ssid_data.get("networkId")
            ssid_number = ssid_data.get("number")
            if not network_id or ssid_number is None:
                continue

            from .meraki_ssid_name import MerakiSSIDNameText
            text_entities.append(
                MerakiSSIDNameText(
                    coordinator,
                    meraki_client,
                    config_entry,
                    ssid_data,
                )
            )

    if text_entities:
        async_add_entities(text_entities)

    return True
