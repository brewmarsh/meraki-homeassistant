"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
