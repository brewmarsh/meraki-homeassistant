"""The select platform for the Meraki integration."""

from __future__ import annotations

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, ENTITY_CHUNK_DELAY, ENTITY_CHUNK_SIZE
from ..helpers.logging_helper import MerakiLoggers
from .meraki_content_filtering import MerakiContentFilteringSelect

_LOGGER = MerakiLoggers.SWITCH


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki select entities."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = coordinator.api

    if coordinator.data:
        select_entities = []
        for network in coordinator.data.get("networks", []):
            select_entities.append(
                MerakiContentFilteringSelect(
                    coordinator,
                    meraki_client,
                    config_entry,
                    network,
                )
            )

        if select_entities:
            _LOGGER.debug("Adding %d select entities", len(select_entities))
            for i in range(0, len(select_entities), ENTITY_CHUNK_SIZE):
                chunk = select_entities[i : i + ENTITY_CHUNK_SIZE]
                async_add_entities(chunk)
                if len(select_entities) > ENTITY_CHUNK_SIZE:
                    await asyncio.sleep(ENTITY_CHUNK_DELAY)
