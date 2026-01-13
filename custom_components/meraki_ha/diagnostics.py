"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
<<<<<<< HEAD
from .coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
from .coordinator import MerakiDataUpdateCoordinator
=======
from .meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)


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
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
=======
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][entry.entry_id][
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        "coordinator"
    ]
    return {
        "config_entry": entry.as_dict(),
        "coordinator_data": coordinator.data,
    }
