"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any, Final

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinators import MerakiMainCoordinator

TO_REDACT: Final = {
    "api_key",
    "serial",
    "serial_number",
    "mac",
    "macaddress",
    "mac_address",
    "password",
    "latitude",
    "longitude",
    "organizationId",
    "organization_id",
    "networkId",
    "network_id",
}


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
    return async_redact_data(
        {
            "config_entry": entry.as_dict(),
            "coordinator_data": coordinator.data,
        },
        TO_REDACT,
    )
