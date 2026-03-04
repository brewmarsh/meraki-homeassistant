"""WebSocket API for Meraki HA."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, callback

from .commands_camera import async_register_camera_commands
from .commands_config import async_register_config_commands
from .commands_guest import async_register_guest_commands
from .commands_network import async_register_network_commands


@callback
def async_setup_websocket_api(hass: HomeAssistant) -> None:
    """Set up the WebSocket API."""
    async_register_camera_commands(hass)
    async_register_config_commands(hass)
    async_register_guest_commands(hass)
    async_register_network_commands(hass)
