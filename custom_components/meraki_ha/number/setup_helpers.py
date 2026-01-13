"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
