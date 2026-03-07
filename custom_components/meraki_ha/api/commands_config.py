"""Configuration-related WebSocket commands for Meraki HA."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import async_get_integration

from custom_components.meraki_ha.const.integration import DOMAIN, from custom_components.meraki_ha.const.websocket import WS_CMD_GET_CONFIG, WS_CMD_GET_VERSION, WS_CMD_SUBSCRIBE_MERAKI_DATA, WS_CMD_UPDATE_ENABLED_NETWORKS, WS_CMD_UPDATE_OPTIONS
from ..helpers.serialization import to_serializable
from .utils import handle_ws_error

if TYPE_CHECKING:
    from ..coordinators.main import MerakiMainCoordinator


@callback
def async_register_config_commands(hass: HomeAssistant) -> None:
    """Register configuration commands."""
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_CONFIG,
        ws_get_config,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_GET_CONFIG,
                vol.Required("config_entry_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_SUBSCRIBE_MERAKI_DATA,
        ws_subscribe_meraki_data,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_SUBSCRIBE_MERAKI_DATA,
                vol.Required("config_entry_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_VERSION,
        ws_get_version,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, WS_CMD_GET_VERSION),
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_UPDATE_OPTIONS,
        ws_update_options,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_UPDATE_OPTIONS,
                vol.Required("config_entry_id"): str,
                vol.Required("options"): dict,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_UPDATE_ENABLED_NETWORKS,
        ws_update_enabled_networks,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_UPDATE_ENABLED_NETWORKS,
                vol.Required("config_entry_id"): str,
                vol.Required("enabled_networks"): [str],
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
@handle_ws_error
async def ws_get_config(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_config command."""
    config_entry_id = msg["config_entry_id"]

    if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiMainCoordinator = hass.data[DOMAIN][config_entry_id][
        "main_coordinator"
    ]
    data = to_serializable(coordinator.data)
    connection.send_result(msg["id"], data)


@callback
def ws_subscribe_meraki_data(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Subscribe to Meraki data updates."""
    try:
        config_entry_id = msg["config_entry_id"]

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        coordinator: MerakiMainCoordinator = hass.data[DOMAIN][config_entry_id][
            "main_coordinator"
        ]

        @callback
        def async_send_update() -> None:
            """Send update to client."""
            data = to_serializable(coordinator.data)
            connection.send_message(websocket_api.event_message(msg["id"], data))

        # Send initial data
        data = to_serializable(coordinator.data)
        connection.send_result(msg["id"], data)

        # Register for updates
        cancel_subscription = coordinator.async_add_listener(async_send_update)
        connection.subscriptions[msg["id"]] = cancel_subscription
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
@handle_ws_error
async def ws_get_version(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_version command."""
    integration = await async_get_integration(hass, DOMAIN)
    version = str(integration.version)
    connection.send_result(msg["id"], {"version": version})


@websocket_api.async_response
@handle_ws_error
async def ws_update_options(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle update_options command."""
    config_entry_id = msg["config_entry_id"]
    options = msg["options"]

    entry = hass.config_entries.async_get_entry(config_entry_id)
    if not entry:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    hass.config_entries.async_update_entry(entry, options=options)
    connection.send_result(msg["id"], {"success": True})


@websocket_api.async_response
@handle_ws_error
async def ws_update_enabled_networks(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle update_enabled_networks command."""
    config_entry_id = msg["config_entry_id"]
    enabled_networks = msg["enabled_networks"]

    entry = hass.config_entries.async_get_entry(config_entry_id)
    if not entry:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    new_options = dict(entry.options)
    new_options["enabled_networks"] = enabled_networks
    hass.config_entries.async_update_entry(entry, options=new_options)
    connection.send_result(msg["id"], {"success": True})
