"""Diagnostics support for Meraki."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_ENABLE_MQTT, DOMAIN
from .meraki_data_coordinator import MerakiDataCoordinator


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
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    diagnostics: dict[str, Any] = {
        "config_entry": entry.as_dict(),
        "coordinator_data": coordinator.data,
    }

    # Add MQTT status if enabled
    mqtt_enabled = entry.options.get(CONF_ENABLE_MQTT, False)
    diagnostics["mqtt"] = {
        "enabled": mqtt_enabled,
    }

    if mqtt_enabled:
        # Add MQTT service status
        mqtt_service = hass.data[DOMAIN][entry.entry_id].get("mqtt_service")
        if mqtt_service:
            diagnostics["mqtt"]["service_running"] = True

        # Add relay manager status
        relay_manager = hass.data[DOMAIN][entry.entry_id].get("mqtt_relay_manager")
        if relay_manager:
            diagnostics["mqtt"]["relay_destinations"] = (
                relay_manager.get_health_status()
            )
        else:
            diagnostics["mqtt"]["relay_destinations"] = {}

    return diagnostics
