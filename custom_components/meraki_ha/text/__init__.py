# custom_components/meraki_ha/text/__init__.py
"""Set up Meraki text entities."""
import logging

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
    _LOGGER.info("text/__init__.py: Setting up Meraki text platform.")
    setup_successful = False # Default to False
    try:
        setup_successful = await ssid_name_async_setup_entry(hass, config_entry, async_add_entities)
        _LOGGER.debug("text/__init__.py: ssid_name_async_setup_entry reported: %s", setup_successful)
        if not setup_successful:
            _LOGGER.warning("text/__init__.py: Setup of SSID name entities reported failure by meraki_ssid_name.py.")
            # For current diagnostics, we still return True from the platform's __init__
            # to see if HA core still complains when main __init__ returns True.
            # In a final version, if setup_successful is False, this function should also return False.
    except Exception as e:
        _LOGGER.error("text/__init__.py: Error during call to ssid_name_async_setup_entry: %s", e, exc_info=True)
        # For current diagnostics, still return True from platform's __init__

    _LOGGER.info("text/__init__.py: Finished setting up Meraki text platform.")
    return True # Diagnostic: always return True from text/__init__.py for now
