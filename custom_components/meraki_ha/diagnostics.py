"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const.integration import DOMAIN

from ..coordinators import MerakiMainCoordinator


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
    coordinator: MerakiMainCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    return {
        "config_entry": entry.as_dict(),
        "coordinator_data": coordinator.data,
    }
