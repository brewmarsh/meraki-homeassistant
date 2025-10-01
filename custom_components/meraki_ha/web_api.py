"""
This module implements the REST API for the Meraki Home Assistant integration's Web UI.
"""
import logging
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from voluptuous import Schema, All, Required, ALLOW_EXTRA

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def async_setup_api(hass: HomeAssistant):
    """Set up the Meraki Web UI API."""
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_config",
        handle_get_config,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_config"),
                Required("config_entry_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
async def handle_get_config(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict):
    """Handle get_config command."""
    config_entry_id = msg["config_entry_id"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(
            msg["id"], "not_found", "Config entry not found"
        )
        return

    coordinator = hass.data[DOMAIN][config_entry_id]["coordinator"]
    connection.send_result(msg["id"], coordinator.data)
