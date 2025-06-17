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
    # Call the setup for SSID Name text entities
    setup_successful = await ssid_name_async_setup_entry(hass, config_entry, async_add_entities)
    _LOGGER.debug("text/__init__.py: ssid_name_async_setup_entry reported: %s", setup_successful)

    # Decide what this platform setup should return.
    # If ssid_name_async_setup_entry is the only thing this platform does,
    # its success should determine the platform's success.
    # However, the plan was to make things return True to see where the HA core error comes from.
    # For this step, let's keep it returning True but log the internal result.
    if not setup_successful:
        _LOGGER.warning("text/__init__.py: Setup of SSID name entities reported failure, but platform setup will still return True for diagnostics.")

    _LOGGER.info("text/__init__.py: Finished setting up Meraki text platform.")
    return True # Explicitly return True, but log internal success/failure.
