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
from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .meraki_ssid_name import MerakiSSIDNameText

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
        coordinator: MerakiDataCoordinator = entry_data.get("coordinator")
    except KeyError as e:
        _LOGGER.error(
            "Text platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e,
        )
        return False

    new_entities: list = []

    if coordinator and coordinator.data and "ssids" in coordinator.data:
        ssids = coordinator.data["ssids"]
        for ssid_data in ssids:
            if not isinstance(ssid_data, dict):
                continue
            network_id = ssid_data.get("networkId")
            ssid_number = ssid_data.get("number")
            if not network_id or ssid_number is None:
                continue

            new_entities.append(
                MerakiSSIDNameText(
                    coordinator,
                    meraki_client,
                    config_entry,
                    ssid_data,
                )
            )
    else:
        _LOGGER.info("No SSIDs found for setting up text entities.")

    if new_entities:
        async_add_entities(new_entities)

    return True
