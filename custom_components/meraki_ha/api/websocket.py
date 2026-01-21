"""WebSocket API for Meraki HA."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import async_get_integration

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.serialization import to_serializable
from ..services.camera_service import CameraService


@callback
def async_setup_websocket_api(hass: HomeAssistant) -> None:
    """Set up the WebSocket API."""
    # Register the command to subscribe to Meraki data
    websocket_api.async_register_command(
        hass,
        "meraki_ha/subscribe_meraki_data",
        ws_subscribe_meraki_data,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/subscribe_meraki_data",
                vol.Required("config_entry_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to get camera stream URL
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_camera_stream_url",
        ws_get_camera_stream_url,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, "meraki_ha/get_camera_stream_url"),
                vol.Required("config_entry_id"): str,
                vol.Required("serial"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to get camera snapshot
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_camera_snapshot",
        ws_get_camera_snapshot,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, "meraki_ha/get_camera_snapshot"),
                vol.Required("config_entry_id"): str,
                vol.Required("serial"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to get version
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_version",
        ws_get_version,
        vol.Schema(
            {
                vol.Required("type"): vol.All(str, "meraki_ha/get_version"),
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@callback
def ws_subscribe_meraki_data(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Subscribe to Meraki data updates."""
    config_entry_id = msg["config_entry_id"]

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
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


@websocket_api.async_response
async def ws_get_camera_stream_url(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle get_camera_stream_url command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    camera_service: CameraService = hass.data[DOMAIN][config_entry_id]["camera_service"]
    stream_url = await camera_service.get_video_stream_url(serial)
    connection.send_result(msg["id"], {"url": stream_url})


@websocket_api.async_response
async def ws_get_camera_snapshot(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle get_camera_snapshot command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    camera_service: CameraService = hass.data[DOMAIN][config_entry_id]["camera_service"]
    snapshot_url = await camera_service.get_camera_snapshot(serial)
    connection.send_result(msg["id"], {"url": snapshot_url})


@websocket_api.async_response
async def ws_get_version(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_version command."""
    integration = await async_get_integration(hass, DOMAIN)
    version = str(integration.version)
    connection.send_result(msg["id"], {"version": version})
