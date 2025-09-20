"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.text import TextEntity

from ..const import DOMAIN, DATA_COORDINATOR
from .meraki_ssid_name import MerakiSSIDNameText


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data[DATA_COORDINATOR]

    text_entities = []
    ssids = coordinator.data.get("ssids", [])
    for ssid in ssids:
        text_entities.append(MerakiSSIDNameText(coordinator, config_entry, ssid))

    if text_entities:
        async_add_entities(text_entities)

    return True
