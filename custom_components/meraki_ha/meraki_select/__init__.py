"""The select platform for the Meraki integration."""

from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.meraki_ha.const.integration import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki select entities."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return

    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovery_service = entry_data["discovery_service"]

    # Entities have already been discovered in __init__.py
    select_entities = []
    for entity in discovery_service.all_entities:
        try:
            if isinstance(entity, SelectEntity):
                select_entities.append(entity)
        except Exception as err:
            _LOGGER.error("Error processing discovered select entity: %s", err)

    if select_entities:
        _LOGGER.debug("Adding %d select entities", len(select_entities))
        async_add_entities(select_entities)
