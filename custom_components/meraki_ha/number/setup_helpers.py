"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
