"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
from ..meraki_data_coordinator import MerakiDataCoordinator
=======
from ..coordinator import MerakiDataUpdateCoordinator
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
=======
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
