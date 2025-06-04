# custom_components/meraki_ha/text/__init__.py
"""Set up Meraki text entities."""
import logging # asyncio removed

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Import the async_setup_entry from the specific text module
from .meraki_ssid_name import async_setup_entry as ssid_name_async_setup_entry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    _LOGGER.info("Setting up Meraki text platform.")

    # Call the setup for SSID Name text entities
    # This directly calls the async_setup_entry from meraki_ssid_name.py
    await ssid_name_async_setup_entry(hass, config_entry, async_add_entities)

    _LOGGER.info("Finished setting up Meraki text platform.")
    return True  # Must return True if setup is successful
