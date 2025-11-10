"""REST API for the Meraki Home Assistant integration's Web UI."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import aiofiles
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from voluptuous import ALLOW_EXTRA, All, Required, Schema

from .const import CONF_ENABLED_NETWORKS, DOMAIN
from .coordinator import MerakiDataUpdateCoordinator
from .services.camera_service import CameraService

_LOGGER = logging.getLogger(__name__)


def async_setup_api(hass: HomeAssistant) -> None:
    """
    Set up the Meraki Web UI API.

    Args:
    ----
        hass: The Home Assistant instance.

    """
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
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_camera_stream_url",
        handle_get_camera_stream_url,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_camera_stream_url"),
                Required("config_entry_id"): str,
                Required("serial"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_camera_snapshot",
        handle_get_camera_snapshot,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_camera_snapshot"),
                Required("config_entry_id"): str,
                Required("serial"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/update_enabled_networks",
        handle_update_enabled_networks,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/update_enabled_networks"),
                Required("config_entry_id"): str,
                Required("enabled_networks"): [str],
            },
            extra=ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
async def handle_get_config(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle get_config command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    enabled_networks = config_entry.options.get(CONF_ENABLED_NETWORKS)

    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    async with aiofiles.open(manifest_path, mode="r") as f:
        contents = await f.read()
    manifest = json.loads(contents)
    version = manifest.get("version")

    connection.send_result(
        msg["id"],
        {
            **coordinator.data,
            "enabled_networks": enabled_networks,
            "config_entry_id": config_entry_id,
            "version": version,
        },
    )


@websocket_api.async_response
async def handle_get_camera_stream_url(
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
async def handle_get_camera_snapshot(
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
async def handle_update_enabled_networks(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle update_enabled_networks command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    enabled_networks = msg["enabled_networks"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    hass.config_entries.async_update_entry(
        config_entry,
        options={
            **config_entry.options,
            CONF_ENABLED_NETWORKS: enabled_networks,
        },
    )
    connection.send_result(msg["id"], {"success": True})
