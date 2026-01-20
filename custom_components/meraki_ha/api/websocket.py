"""WebSocket API for Meraki HA."""

# Ensure this file is tracked by git
from __future__ import annotations

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..const import DOMAIN


@callback
def async_setup_websocket_api(hass: HomeAssistant) -> None:
    """Set up the WebSocket API."""
    # Register the command to subscribe to Meraki data
    websocket_api.async_register_command(hass, ws_subscribe_meraki_data)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "meraki_ha/subscribe_meraki_data",
        vol.Required("config_entry_id"): str,
    }
)
@callback
def ws_subscribe_meraki_data(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Subscribe to Meraki data updates."""
    config_entry_id = msg["config_entry_id"]

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]

    @callback
    def async_send_update() -> None:
        """Send update to client."""
        connection.send_message(
            websocket_api.event_message(msg["id"], coordinator.data)
        )

    # Send initial data
    connection.send_result(msg["id"], coordinator.data)

    # Register for updates
    cancel_subscription = coordinator.async_add_listener(async_send_update)
    connection.subscriptions[msg["id"]] = cancel_subscription
