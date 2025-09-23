"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .meraki_ssid_name import MerakiSSIDNameText


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = coordinator.api

    if coordinator.data:
        text_entities = [
            MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid)
            for ssid in coordinator.data.get("ssids", [])
        ]

        if text_entities:
            async_add_entities(text_entities)

    return True
