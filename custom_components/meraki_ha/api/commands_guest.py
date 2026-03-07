"""Guest/IPSK-related WebSocket commands for Meraki HA."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from ..const.integration import (
    DOMAIN,
    WS_CMD_CREATE_GUEST_KEY,
    WS_CMD_GET_GUEST_KEYS,
    WS_CMD_REVOKE_GUEST_KEY,
)
from ..helpers.serialization import to_serializable
from .utils import handle_ws_error

if TYPE_CHECKING:
    from ..services.ipsk_manager import IPSKManager

_LOGGER = logging.getLogger(__name__)


@callback
def async_register_guest_commands(hass: HomeAssistant) -> None:
    """Register guest/IPSK commands."""
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_GUEST_KEYS,
        ws_get_guest_keys,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_GET_GUEST_KEYS,
                vol.Optional("config_entry_id"): str,
                vol.Optional("network_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_CREATE_GUEST_KEY,
        ws_create_guest_key,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_CREATE_GUEST_KEY,
                vol.Required("config_entry_id"): str,
                vol.Required("network_id"): str,
                vol.Required("ssid_number"): str,
                vol.Required("duration_minutes"): int,
                vol.Optional("name"): str,
                vol.Optional("passphrase"): str,
                vol.Optional("group_policy_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_REVOKE_GUEST_KEY,
        ws_revoke_guest_key,
        vol.Schema(
            {
                vol.Required("type"): WS_CMD_REVOKE_GUEST_KEY,
                vol.Required("identity_psk_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
@handle_ws_error
async def ws_get_guest_keys(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle IPSK/get command."""
    config_entry_id = msg.get("config_entry_id")
    network_id = msg.get("network_id")

    if "ipsk_manager" not in hass.data.get(DOMAIN, {}):
        connection.send_error(
            msg["id"], "not_initialized", "IPSK Manager not initialized"
        )
        return

    manager: IPSKManager = hass.data[DOMAIN]["ipsk_manager"]
    keys = manager.get_active_keys(config_entry_id, network_id)
    connection.send_result(msg["id"], to_serializable(keys))


@websocket_api.async_response
@handle_ws_error
async def ws_create_guest_key(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle IPSK/create command."""
    if "ipsk_manager" not in hass.data.get(DOMAIN, {}):
        connection.send_error(
            msg["id"], "not_initialized", "IPSK Manager not initialized"
        )
        return

    manager: IPSKManager = hass.data[DOMAIN]["ipsk_manager"]

    try:
        key = await manager.create_guest_key(
            config_entry_id=msg["config_entry_id"],
            network_id=msg["network_id"],
            ssid_number=msg["ssid_number"],
            duration_minutes=msg["duration_minutes"],
            name=msg.get("name", "Guest User"),
            passphrase=msg.get("passphrase"),
            group_policy_id=msg.get("group_policy_id"),
        )
        connection.send_result(msg["id"], to_serializable(key))
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.exception("Error in ws_create_guest_key: %s", err)
        connection.send_error(msg["id"], "creation_failed", str(err))


@websocket_api.async_response
@handle_ws_error
async def ws_revoke_guest_key(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle IPSK/revoke command."""
    identity_psk_id = msg["identity_psk_id"]

    if "ipsk_manager" not in hass.data.get(DOMAIN, {}):
        connection.send_error(
            msg["id"], "not_initialized", "IPSK Manager not initialized"
        )
        return

    manager: IPSKManager = hass.data[DOMAIN]["ipsk_manager"]
    success = await manager.remove_guest_key(identity_psk_id)
    if success:
        connection.send_result(msg["id"], {"success": True})
    else:
        connection.send_error(msg["id"], "revocation_failed", "Failed to revoke key")
