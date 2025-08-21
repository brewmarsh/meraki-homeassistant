"""The select platform for the Meraki integration."""

from __future__ import annotations

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
    meraki_data = hass.data[DOMAIN][config_entry.entry_id]
    main_coordinator = meraki_data["coordinator"]
    cf_coordinators = meraki_data.get("content_filtering_coordinators", {})

    if main_coordinator.data and cf_coordinators:
        select_entities = []
        for network_id, cf_coordinator in cf_coordinators.items():
            # Find the network data from the main coordinator
            network_data = next(
                (
                    n
                    for n in main_coordinator.data.get("networks", [])
                    if n["id"] == network_id
                ),
                None,
            )
            if network_data:
                select_entities.append(
                    MerakiContentFilteringSelect(
                        coordinator=cf_coordinator,
                        config_entry=config_entry,
                        network_data=network_data,
                    )
                )
        async_add_entities(select_entities)
