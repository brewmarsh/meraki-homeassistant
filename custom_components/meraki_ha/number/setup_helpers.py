"""Helper function for setting up all number entities."""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
) -> List[Entity]:
    """Set up all number entities from the central coordinator."""
    return []