"""The select platform for the Meraki integration."""

from __future__ import annotations

import logging
import asyncio

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
    meraki_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = meraki_data["coordinator"]
    meraki_client = meraki_data["client"]

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
            chunk_size = 50
            for i in range(0, len(select_entities), chunk_size):
                chunk = select_entities[i:i + chunk_size]
                async_add_entities(chunk)
                if len(select_entities) > chunk_size:
                    await asyncio.sleep(1)
