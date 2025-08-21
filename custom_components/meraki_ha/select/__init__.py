"""The select platform for the Meraki integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .meraki_content_filtering import MerakiSsidContentFilteringSelect
from .meraki_network_content_filtering import MerakiNetworkContentFilteringSelect

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki select entities."""
    meraki_data = hass.data[DOMAIN][config_entry.entry_id]
    main_coordinator = meraki_data["coordinator"]
    ssid_cf_coordinators = meraki_data.get("ssid_content_filtering_coordinators", {})
    network_cf_coordinators = meraki_data.get(
        "network_content_filtering_coordinators", {}
    )

    select_entities = []

    # Set up per-SSID select entities
    if main_coordinator.data and ssid_cf_coordinators:
        for ssid_key, cf_coordinator in ssid_cf_coordinators.items():
            ssid_data = cf_coordinator.data
            if ssid_data:
                select_entities.append(
                    MerakiSsidContentFilteringSelect(
                        coordinator=cf_coordinator,
                        config_entry=config_entry,
                        ssid_data=ssid_data,
                    )
                )

    # Set up network-wide select entities
    if main_coordinator.data and network_cf_coordinators:
        for network_id, cf_coordinator in network_cf_coordinators.items():
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
                    MerakiNetworkContentFilteringSelect(
                        coordinator=cf_coordinator,
                        config_entry=config_entry,
                        network_data=network_data,
                    )
                )

    async_add_entities(select_entities)
