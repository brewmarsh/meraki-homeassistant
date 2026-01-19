"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
<<<<<<< HEAD
from .coordinator import MerakiDataUpdateCoordinator
=======
from .meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """
    Return diagnostics for a config entry.

    Args:
    ----
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns
    -------
        A dictionary of diagnostics.

    """
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
=======
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][entry.entry_id][
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        "coordinator"
    ]
    return {
        "config_entry": entry.as_dict(),
        "coordinator_data": coordinator.data,
    }
