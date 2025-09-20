"""Button platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.button import ButtonEntity

from ..const import DOMAIN, DATA_COORDINATOR
from .reboot import MerakiRebootButton


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki button entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data[DATA_COORDINATOR]

    button_entities = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        button_entities.append(MerakiRebootButton(coordinator.api, device_info, config_entry))

    if button_entities:
        async_add_entities(button_entities)

    return True
