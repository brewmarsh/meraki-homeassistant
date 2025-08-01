"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_CLIENT,
)
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.network import MerakiNetworkCoordinator
from .meraki_ssid_name import MerakiSSIDName

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    try:
        entry_data = hass.data[DOMAIN][config_entry.entry_id]
        meraki_client: MerakiAPIClient = entry_data[DATA_CLIENT]
        network_coordinator: MerakiNetworkCoordinator = entry_data.get(
            "network_coordinator"
        )
    except KeyError as e:
        _LOGGER.error(
            "Text platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e,
        )
        return False

    new_entities: list = []

    if network_coordinator and network_coordinator.data:
        for ssid_unique_id, ssid_data in network_coordinator.data.items():
            if not isinstance(ssid_data, dict):
                continue
            new_entities.append(
                MerakiSSIDName(
                    network_coordinator,
                    meraki_client,
                    config_entry,
                    ssid_unique_id,
                    ssid_data,
                )
            )
    else:
        _LOGGER.info("No SSIDs found for setting up text entities.")

    if new_entities:
        async_add_entities(new_entities)

    return True
