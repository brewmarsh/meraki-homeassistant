"""REST API for the Meraki Home Assistant integration's Web UI."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import aiofiles  # type: ignore[import-untyped]
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from voluptuous import ALLOW_EXTRA, All, Optional, Required, Schema

from .const import (
    CONF_CAMERA_LINK_INTEGRATION,
    CONF_DASHBOARD_DEVICE_TYPE_FILTER,
    CONF_DASHBOARD_STATUS_FILTER,
    CONF_DASHBOARD_VIEW_MODE,
    CONF_ENABLED_NETWORKS,
    CONF_SCAN_INTERVAL,
    DATA_CLIENT,
    DEFAULT_CAMERA_LINK_INTEGRATION,
    DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER,
    DEFAULT_DASHBOARD_STATUS_FILTER,
    DEFAULT_DASHBOARD_VIEW_MODE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .core.errors import MerakiError
from .core.timed_access_manager import TimedAccessManager
from .meraki_data_coordinator import MerakiDataCoordinator
from .services.camera_service import CameraService

_LOGGER = logging.getLogger(__name__)

# Storage file for camera mappings (avoids config entry reload on update)
CAMERA_MAPPINGS_STORAGE = "meraki_camera_mappings.json"


async def _get_camera_mappings_path(hass: HomeAssistant) -> Path:
    """Get the path to the camera mappings storage file."""
    return Path(hass.config.path(".storage")) / CAMERA_MAPPINGS_STORAGE


async def _load_camera_mappings(hass: HomeAssistant) -> dict[str, dict[str, str]]:
    """Load camera mappings from storage file."""
    storage_path = await _get_camera_mappings_path(hass)
    if not storage_path.exists():
        return {}
    try:
        async with aiofiles.open(storage_path) as f:
            content = await f.read()
            return json.loads(content) if content else {}
    except (json.JSONDecodeError, OSError) as e:
        _LOGGER.warning("Failed to load camera mappings: %s", e)
        return {}


async def _save_camera_mappings(
    hass: HomeAssistant, mappings: dict[str, dict[str, str]]
) -> None:
    """Save camera mappings to storage file."""
    storage_path = await _get_camera_mappings_path(hass)
    try:
        async with aiofiles.open(storage_path, "w") as f:
            await f.write(json.dumps(mappings, indent=2))
    except OSError as e:
        _LOGGER.error("Failed to save camera mappings: %s", e)


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
                Optional("stream_source"): str,  # "rtsp" or "cloud"
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
    websocket_api.async_register_command(
        hass,
        "meraki_ha/create_timed_access_key",
        handle_create_timed_access_key,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/create_timed_access_key"),
                Required("config_entry_id"): str,
                Required("network_id"): str,
                Required("ssid_number"): str,
                Required("name"): str,
                Required("passphrase"): str,
                Required("duration_hours"): int,
                Optional("group_policy_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_camera_mappings",
        handle_get_camera_mappings,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_camera_mappings"),
                Required("config_entry_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/set_camera_mapping",
        handle_set_camera_mapping,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/set_camera_mapping"),
                Required("config_entry_id"): str,
                Required("serial"): str,
                Required("linked_entity_id"): str,  # Empty string to remove mapping
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_available_cameras",
        handle_get_available_cameras,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_available_cameras"),
                Optional("integration_filter"): str,
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

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return
    enabled_networks = config_entry.options.get(CONF_ENABLED_NETWORKS)
    if enabled_networks is None:
        enabled_networks = [
            n["id"] for n in coordinator.data.get("networks", []) if "id" in n
        ]

    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    async with aiofiles.open(manifest_path) as f:
        contents = await f.read()
    manifest = json.loads(contents)
    version = manifest.get("version")

    # Get dashboard settings from options
    dashboard_settings = {
        "dashboard_view_mode": config_entry.options.get(
            CONF_DASHBOARD_VIEW_MODE, DEFAULT_DASHBOARD_VIEW_MODE
        ),
        "dashboard_device_type_filter": config_entry.options.get(
            CONF_DASHBOARD_DEVICE_TYPE_FILTER, DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER
        ),
        "dashboard_status_filter": config_entry.options.get(
            CONF_DASHBOARD_STATUS_FILTER, DEFAULT_DASHBOARD_STATUS_FILTER
        ),
        "camera_link_integration": config_entry.options.get(
            CONF_CAMERA_LINK_INTEGRATION, DEFAULT_CAMERA_LINK_INTEGRATION
        ),
    }

    # Get refresh timing info
    scan_interval = config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    last_updated = (
        coordinator.last_update_success_time.isoformat()
        if coordinator.last_update_success_time
        else None
    )

    connection.send_result(
        msg["id"],
        {
            **coordinator.data,
            "enabled_networks": enabled_networks,
            "config_entry_id": config_entry_id,
            "version": version,
            "scan_interval": scan_interval,
            "last_updated": last_updated,
            **dashboard_settings,
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
        msg: The WebSocket message containing:
            - config_entry_id: The config entry ID
            - serial: The camera serial number
            - stream_source (optional): "rtsp" or "cloud" to specify the stream type

    Note: Cloud URLs are Meraki Dashboard links meant for browser viewing.
    They cannot be used directly in Home Assistant's stream component.
    RTSP URLs can be used for direct video streaming if enabled on the camera.

    """
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]
    stream_source = msg.get("stream_source")
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    camera_service: CameraService = hass.data[DOMAIN][config_entry_id]["camera_service"]

    # If a specific stream source is requested, use that
    if stream_source == "cloud":
        stream_url = await camera_service.get_cloud_video_url(serial)
    elif stream_source == "rtsp":
        stream_url = await camera_service.get_rtsp_stream_url(serial)
    else:
        # Default: try cloud first, then fall back to RTSP
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


@websocket_api.async_response
async def handle_create_timed_access_key(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle create_timed_access_key command.

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

    api_client = hass.data[DOMAIN][config_entry_id][DATA_CLIENT]
    manager = TimedAccessManager(api_client)

    try:
        result = await manager.create_timed_access_key(
            network_id=msg["network_id"],
            ssid_number=msg["ssid_number"],
            name=msg["name"],
            passphrase=msg["passphrase"],
            duration_hours=msg["duration_hours"],
            group_policy_id=msg.get("group_policy_id"),
        )
        connection.send_result(msg["id"], result)
    except (ValueError, KeyError, TypeError) as e:
        _LOGGER.error("Invalid input for timed access key: %s", e)
        connection.send_error(msg["id"], "invalid_input", str(e))
    except MerakiError as e:
        _LOGGER.error("Meraki API error creating timed access key: %s", e)
        connection.send_error(msg["id"], "api_error", str(e))


@websocket_api.async_response
async def handle_get_camera_mappings(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Get camera entity mappings (Meraki serial -> linked HA entity_id).

    This allows users to link Meraki cameras to other camera entities
    (e.g., Blue Iris cameras that receive the RTSP stream).
    """
    config_entry_id = msg["config_entry_id"]
    all_mappings = await _load_camera_mappings(hass)
    mappings = all_mappings.get(config_entry_id, {})
    connection.send_result(msg["id"], {"mappings": mappings})


@websocket_api.async_response
async def handle_set_camera_mapping(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Set a camera entity mapping (link Meraki camera to another HA camera).

    Args:
        serial: The Meraki camera serial number
        linked_entity_id: The HA entity_id to link to (e.g., camera.blue_iris_front)
                         Pass empty string to remove the mapping.
    """
    config_entry_id = msg["config_entry_id"]
    serial = msg["serial"]
    linked_entity_id = msg["linked_entity_id"]

    # Load all mappings from storage
    all_mappings = await _load_camera_mappings(hass)

    # Get mappings for this config entry
    mappings = dict(all_mappings.get(config_entry_id, {}))

    # Update or remove mapping
    if linked_entity_id:
        mappings[serial] = linked_entity_id
    elif serial in mappings:
        del mappings[serial]

    # Save updated mappings to storage (not config entry - avoids reload!)
    all_mappings[config_entry_id] = mappings
    await _save_camera_mappings(hass, all_mappings)

    connection.send_result(msg["id"], {"success": True, "mappings": mappings})


@websocket_api.async_response
async def handle_get_available_cameras(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Get all available camera entities in Home Assistant.

    Returns a list of camera entities that can be linked to Meraki cameras.
    Excludes Meraki cameras themselves to avoid circular links.

    Args:
        integration_filter: Optional integration domain to filter cameras by
                           (e.g., 'blue_iris', 'generic'). Empty string shows all.
    """
    integration_filter = msg.get("integration_filter", "").lower().strip()
    camera_entities = []

    # Get entity registry to look up integration/platform
    entity_registry = er.async_get(hass)

    # Get all camera entities from the state machine
    for state in hass.states.async_all("camera"):
        entity_id = state.entity_id
        # Skip Meraki cameras (they have our domain prefix pattern)
        if "meraki" in entity_id.lower():
            continue

        # If integration filter is set, check if entity belongs to that integration
        if integration_filter:
            # Normalize filter for flexible matching (blue_iris matches blueiris)
            normalized_filter = integration_filter.replace("_", "").replace("-", "")
            entity_entry = entity_registry.async_get(entity_id)
            if entity_entry:
                # Check platform (integration domain)
                platform = entity_entry.platform.lower()
                normalized_platform = platform.replace("_", "").replace("-", "")
                filter_matches = (
                    normalized_filter in normalized_platform
                    or normalized_platform in normalized_filter
                )
                if not filter_matches:
                    continue
            else:
                # No registry entry, try to match by entity_id pattern
                normalized_entity = entity_id.lower().replace("_", "").replace("-", "")
                if normalized_filter not in normalized_entity:
                    continue

        friendly_name = state.attributes.get("friendly_name", entity_id)
        camera_entities.append(
            {
                "entity_id": entity_id,
                "friendly_name": friendly_name,
                "state": state.state,
            }
        )

    # Sort by friendly name
    camera_entities.sort(key=lambda x: x["friendly_name"].lower())

    connection.send_result(msg["id"], {"cameras": camera_entities})
