"""Network-related WebSocket commands for Meraki HA."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from custom_components.meraki_ha.const.api import DATA_CLIENT
from custom_components.meraki_ha.const.websocket import (
    WS_CMD_GET_NETWORK_EVENTS,
    WS_CMD_TIMED_ACCESS_GET_POLICIES,
)
from ..helpers.serialization import to_serializable
from .utils import get_config_entry_data, handle_ws_error

if TYPE_CHECKING:
    from ..core.api import MerakiApiClientProtocol


@callback
def async_register_network_commands(hass: HomeAssistant) -> None:
    """Register network commands."""
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_NETWORK_EVENTS,
        ws_get_network_events,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_GET_NETWORK_EVENTS,
                vol.Required("config_entry_id"): str,
                vol.Optional("network_id"): str,
                vol.Optional("per_page"): int,
                vol.Optional("product_type"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_TIMED_ACCESS_GET_POLICIES,
        ws_timed_access_get_policies,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_TIMED_ACCESS_GET_POLICIES,
                vol.Required("config_entry_id"): str,
                vol.Required("network_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
@handle_ws_error
async def ws_get_network_events(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_network_events command."""
    config_entry_id = msg["config_entry_id"]
    network_id = msg.get("network_id")

    if not network_id:
        connection.send_error(msg["id"], "invalid_payload", "Network ID is required")
        return

    client: MerakiApiClientProtocol | None = get_config_entry_data(
        hass, connection, msg, config_entry_id, DATA_CLIENT
    )
    if client is None:
        return

    params = {}
    if "per_page" in msg:
        params["per_page"] = msg["per_page"]
    if "product_type" in msg:
        params["product_type"] = msg["product_type"]

    events = await client.network.get_network_events(network_id, **params)
    connection.send_result(msg["id"], to_serializable(events))


@websocket_api.async_response
@handle_ws_error
async def ws_timed_access_get_policies(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle timed_access/get_policies command."""
    config_entry_id = msg["config_entry_id"]
    network_id = msg["network_id"]

    client: MerakiApiClientProtocol | None = get_config_entry_data(
        hass, connection, msg, config_entry_id, DATA_CLIENT
    )
    if client is None:
        return

    policies = await client.network.get_group_policies(network_id)
    connection.send_result(msg["id"], to_serializable(policies))
