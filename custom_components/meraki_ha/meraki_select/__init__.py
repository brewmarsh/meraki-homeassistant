"""The select platform for the Meraki integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_ENABLE_VPN_MANAGEMENT, DOMAIN
from .meraki_content_filtering import MerakiContentFilteringSelect
from .vpn import MerakiVpnSelect

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
            if config_entry.options.get(CONF_ENABLE_VPN_MANAGEMENT):
                select_entities.append(
                    MerakiVpnSelect(
                        coordinator,
                        meraki_client,
                        config_entry,
                        network,
                    )
                )

        async_add_entities(select_entities)
