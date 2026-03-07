"""Camera-related WebSocket commands for Meraki HA."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.websocket import (
    WS_CMD_GET_CAMERA_SNAPSHOT,
    WS_CMD_GET_CAMERA_STREAM_URL,
)
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from .utils import handle_ws_error

if TYPE_CHECKING:
    from ..services.camera_service import CameraService


@callback
def async_register_camera_commands(hass: HomeAssistant) -> None:
    """Register camera commands."""
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_CAMERA_STREAM_URL,
        ws_get_camera_stream_url,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, WS_CMD_GET_CAMERA_STREAM_URL),
                vol.Required("config_entry_id"): str,
                vol.Required("serial"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        WS_CMD_GET_CAMERA_SNAPSHOT,
        ws_get_camera_snapshot,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, WS_CMD_GET_CAMERA_SNAPSHOT),
                vol.Required("config_entry_id"): str,
                vol.Required("serial"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
@handle_ws_error
async def ws_get_camera_stream_url(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_camera_stream_url command."""
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]

    if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    camera_service: CameraService = hass.data[DOMAIN][config_entry_id]["camera_service"]
    stream_url = await camera_service.get_video_stream_url(serial)
    connection.send_result(msg["id"], {"url": stream_url})


@websocket_api.async_response
@handle_ws_error
async def ws_get_camera_snapshot(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_camera_snapshot command."""
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]

    if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    camera_service: CameraService = hass.data[DOMAIN][config_entry_id]["camera_service"]
    snapshot_url = await camera_service.get_camera_snapshot(serial)
    connection.send_result(msg["id"], {"url": snapshot_url})
