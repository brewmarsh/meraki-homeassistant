"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_CLIENT, DATA_COORDINATORS
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.network import MerakiNetworkCoordinator
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
        network_coordinator: MerakiNetworkCoordinator = entry_data.get(
            "network_coordinator"
        )
        if not network_coordinator:
            _LOGGER.error(
                "Text platform: Network coordinator not found for entry %s. Cannot set up SSID name text entities.",
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
    if network_coordinator and network_coordinator.data:
        ssids = network_coordinator.data.get("ssids", [])
        for ssid_data in ssids:
            if not isinstance(ssid_data, dict):
                _LOGGER.warning(
                    "Skipping non-dictionary ssid_data in text platform: %s",
                    ssid_data,
                )
                continue

            if not ssid_data.get("enabled"):
                continue

            ssid_unique_id = ssid_data.get("unique_id")
            if not ssid_unique_id:
                _LOGGER.warning(
                    "SSID data missing unique_id, cannot create entity: %s", ssid_data
                )
                continue

            new_entities.append(
                MerakiSSIDNameText(
                    network_coordinator,
                    meraki_client,
                    config_entry,
                    ssid_unique_id,
                    ssid_data,
                )
            )
    else:
        _LOGGER.info(
            "Network Coordinator data not available or no SSIDs found for setting up SSID name text entities."
        )

    if new_entities:
        async_add_entities(new_entities)
        _LOGGER.info("Added %d Meraki text entities.", len(new_entities))
    else:
        _LOGGER.info("No Meraki text entities were added.")

    return True
