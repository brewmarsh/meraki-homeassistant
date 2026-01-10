"""Helper function for setting up all number entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)

_LOGGER = logging.getLogger(__name__)


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
) -> list[Entity]:
    """Set up all number entities from the central coordinator."""
    return []
