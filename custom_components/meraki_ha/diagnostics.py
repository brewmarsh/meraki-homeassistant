"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
<<<<<<< HEAD
from .meraki_data_coordinator import MerakiDataCoordinator
=======
from .coordinator import MerakiDataUpdateCoordinator
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


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
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][entry.entry_id][
=======
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        "coordinator"
    ]
    return {
        "config_entry": entry.as_dict(),
        "coordinator_data": coordinator.data,
    }
