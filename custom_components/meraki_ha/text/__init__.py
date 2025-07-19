"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_CLIENT, DATA_COORDINATORS
from ..api.meraki_api import MerakiAPIClient
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from .meraki_ssid_name import MerakiSSIDNameText

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    _LOGGER.info("Setting up Meraki text platform for entry %s", config_entry.entry_id)

    try:
        entry_data = hass.data[DOMAIN][config_entry.entry_id]
        meraki_client: MerakiAPIClient = entry_data[DATA_CLIENT]

        # Get the SSID device coordinator for SSID name text entities
        ssid_coordinator: SSIDDeviceCoordinator = entry_data[DATA_COORDINATORS].get(
            "ssid_devices"
        )
        if not ssid_coordinator:
            _LOGGER.error(
                "Text platform: SSID Device coordinator not found for entry %s. Cannot set up SSID name text entities.",
                config_entry.entry_id,
            )
            return False  # Or True if other text entities might exist from other coordinators
    except KeyError as e:
        _LOGGER.error(
            "Text platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e,
        )
        return False

    new_entities: list = []

    # Setup SSID Name Text Entities
    if ssid_coordinator and ssid_coordinator.data:
        # _LOGGER.debug("SSID Coordinator data available, setting up SSID name text entities. %s SSIDs found.", len(ssid_coordinator.data)) # Removed
        for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
            if not isinstance(ssid_data, dict):
                _LOGGER.warning(
                    "Skipping non-dictionary ssid_data for SSID unique_id %s in text platform.",
                    ssid_unique_id,
                )
                continue

            # _LOGGER.debug("Setting up text entity for SSID: %s (Data: %s)", ssid_data.get('name', ssid_unique_id), ssid_data) # Removed
            new_entities.append(
                MerakiSSIDNameText(
                    ssid_coordinator,
                    meraki_client,
                    config_entry,
                    ssid_unique_id,
                    ssid_data,
                )
            )
    else:
        _LOGGER.info(
            "SSID Coordinator data not available or no SSIDs found for setting up SSID name text entities."
        )

    if new_entities:
        async_add_entities(new_entities)
        _LOGGER.info("Added %d Meraki text entities.", len(new_entities))
    else:
        _LOGGER.info("No Meraki text entities were added.")

    return True
