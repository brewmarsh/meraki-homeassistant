"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
