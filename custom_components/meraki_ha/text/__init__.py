import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    _LOGGER.info("Attempting to set up Meraki text platform for entry %s", config_entry.entry_id)
    try:
        # Ensure coordinators structure exists and the main coordinator is accessible
        main_coordinator_key = "main" # Or whatever key is used for the main data coordinator
        coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinators"].get(main_coordinator_key)
        if not coordinator:
            _LOGGER.error("Text platform: Main coordinator ('%s') not found for entry %s", main_coordinator_key, config_entry.entry_id)
            return False
    except KeyError as e:
        _LOGGER.error("Text platform: Coordinators structure not found in hass.data for entry %s. Error: %s", config_entry.entry_id, e)
        return False

    # entities = []
    # async_add_entities(entities) # No entities added yet in this version
    _LOGGER.info("Meraki text platform setup nominally complete for entry %s (no entities added in this version).", config_entry.entry_id)
    return True
