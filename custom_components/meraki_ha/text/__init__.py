# custom_components/meraki_ha/text/__init__.py
"""Set up Meraki text entities."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Import the async_setup_entry from the specific text module
# from .meraki_ssid_name import async_setup_entry as ssid_name_async_setup_entry # Commented out

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    _LOGGER.info("text/__init__.py: Ultra-minimal async_setup_entry called, intentionally doing nothing, returning True for diagnostics.")
    return True
