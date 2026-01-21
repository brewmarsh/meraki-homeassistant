"""The select platform for the Meraki integration."""

from __future__ import annotations

<<<<<<< HEAD
import asyncio
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .meraki_content_filtering import MerakiContentFilteringSelect

_LOGGER = logging.getLogger(__name__)


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
<<<<<<< HEAD

        if select_entities:
            _LOGGER.debug("Adding %d select entities", len(select_entities))
            chunk_size = 50
            for i in range(0, len(select_entities), chunk_size):
                chunk = select_entities[i : i + chunk_size]
                async_add_entities(chunk)
                if len(select_entities) > chunk_size:
                    await asyncio.sleep(1)
=======
        async_add_entities(select_entities)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
