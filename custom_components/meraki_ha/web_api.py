"""REST API for the Meraki Home Assistant integration's Web UI."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import aiofiles  # type: ignore[import-untyped]
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from voluptuous import ALLOW_EXTRA, All, Optional, Required, Schema

from .const import CONF_ENABLED_NETWORKS, DATA_CLIENT, DOMAIN
<<<<<<< HEAD
<<<<<<< HEAD
from .core.timed_access_manager import TimedAccessManager
=======
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
from .meraki_data_coordinator import MerakiDataCoordinator
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
    websocket_api.async_register_command(
        hass,
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        "meraki_ha/update_options",
        handle_update_options,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/update_options"),
                Required("config_entry_id"): str,
                Required("options"): dict,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_network_events",
        handle_get_network_events,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/get_network_events"),
                Required("config_entry_id"): str,
                Required("network_id"): str,
                Optional("per_page", default=10): int,
                Optional("starting_after"): str,
                Optional("product_type"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/get_keys",
        handle_get_timed_access_keys,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/timed_access/get_keys"),
                Required("config_entry_id"): str,
                Optional("network_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/create",
        handle_create_timed_access_key,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/timed_access/create"),
                Required("config_entry_id"): str,
                Required("network_id"): str,
                Required("ssid_number"): str,
                Required("duration"): int,
                Optional("name"): str,
                Optional("passphrase"): str,
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
                Optional("group_policy_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/delete",
        handle_delete_timed_access_key,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/timed_access/delete"),
                Required("config_entry_id"): str,
                Required("identity_psk_id"): str,
                Required("network_id"): str,
                Required("ssid_number"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/get_policies",
        handle_get_group_policies,
        Schema(
            {
                Required("type"): All(str, "meraki_ha/timed_access/get_policies"),
                Required("config_entry_id"): str,
                Required("network_id"): str,
            },
            extra=ALLOW_EXTRA,
        ),
    )
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129


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
<<<<<<< HEAD
<<<<<<< HEAD
    config_entry_id = msg["config_entry_id"]
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    _LOGGER.debug(
        "Received meraki_ha/get_config command. Message: %s",
        msg,
    )
    config_entry_id = msg.get("config_entry_id")
    _LOGGER.debug(
        "config_entry_id received: %s (Type: %s)",
        config_entry_id,
        type(config_entry_id),
    )
    if config_entry_id is None:
        _LOGGER.error(
            "Config entry ID is None in meraki_ha/get_config command. Message: %s",
            msg,
        )
        connection.send_error(
            msg["id"],
            "invalid_format",
            "required key not provided @ data['config_entry_id']. Got None",
        )
        return
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
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

    connection.send_result(
        msg["id"],
        {
            **coordinator.data,
            "enabled_networks": enabled_networks,
<<<<<<< HEAD
<<<<<<< HEAD
=======
            "options": dict(config_entry.options),
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
            "options": dict(config_entry.options),
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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


@websocket_api.async_response
<<<<<<< HEAD
<<<<<<< HEAD
async def handle_create_timed_access_key(
=======
async def handle_update_options(
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
async def handle_update_options(
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
<<<<<<< HEAD
<<<<<<< HEAD
    Handle create_timed_access_key command.
=======
    Handle update_options command.
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
    Handle update_options command.
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
<<<<<<< HEAD
<<<<<<< HEAD
=======
    new_options = msg["options"]
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
    new_options = msg["options"]
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

<<<<<<< HEAD
<<<<<<< HEAD
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
    except Exception as e:
        _LOGGER.exception("Error creating timed access key: %s", e)
        connection.send_error(msg["id"], "error", str(e))
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    hass.config_entries.async_update_entry(
        config_entry,
        options={
            **config_entry.options,
            **new_options,
        },
    )
    connection.send_result(msg["id"], {"success": True})


@websocket_api.async_response
async def handle_get_network_events(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle get_network_events command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    network_id = msg["network_id"]
    per_page = msg.get("per_page", 10)
    starting_after = msg.get("starting_after")
    product_type = msg.get("product_type")

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]

    try:
        events = await coordinator.api.get_network_events(
            network_id=network_id,
            product_type=product_type,
            per_page=per_page,
            starting_after=starting_after,
        )
        connection.send_result(msg["id"], events)
    except Exception as e:
        _LOGGER.error("Error fetching network events: %s", e)
        connection.send_error(msg["id"], "fetch_error", str(e))


@websocket_api.async_response
async def handle_get_timed_access_keys(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_timed_access_keys command."""
    config_entry_id = msg["config_entry_id"]
    network_id = msg.get("network_id")

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    manager = hass.data[DOMAIN][config_entry_id].get("timed_access_manager")
    if not manager:
        connection.send_error(msg["id"], "not_found", "Manager not found")
        return

    keys = manager.get_keys(network_id)
    connection.send_result(msg["id"], keys)


@websocket_api.async_response
async def handle_create_timed_access_key(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle create_timed_access_key command."""
    config_entry_id = msg["config_entry_id"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    manager = hass.data[DOMAIN][config_entry_id].get("timed_access_manager")
    if not manager:
        connection.send_error(msg["id"], "not_found", "Manager not found")
        return

    try:
        key = await manager.create_key(
            config_entry_id=config_entry_id,
            network_id=msg["network_id"],
            ssid_number=msg["ssid_number"],
            duration_minutes=msg["duration"],
            name=msg.get("name"),
            passphrase=msg.get("passphrase"),
            group_policy_id=msg.get("group_policy_id"),
        )
        connection.send_result(msg["id"], key.__dict__)
    except Exception as e:
        _LOGGER.error("Error creating timed access key: %s", e)
        connection.send_error(msg["id"], "create_error", str(e))


@websocket_api.async_response
async def handle_delete_timed_access_key(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle delete_timed_access_key command."""
    config_entry_id = msg["config_entry_id"]
    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    manager = hass.data[DOMAIN][config_entry_id].get("timed_access_manager")
    if not manager:
        connection.send_error(msg["id"], "not_found", "Manager not found")
        return

    try:
        await manager.delete_key(
            identity_psk_id=msg["identity_psk_id"],
            network_id=msg["network_id"],
            ssid_number=msg["ssid_number"],
            config_entry_id=config_entry_id,
        )
        connection.send_result(msg["id"], {"success": True})
    except Exception as e:
        _LOGGER.error("Error deleting timed access key: %s", e)
        connection.send_error(msg["id"], "delete_error", str(e))


@websocket_api.async_response
async def handle_get_group_policies(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_group_policies command."""
    config_entry_id = msg["config_entry_id"]
    network_id = msg["network_id"]

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    client = hass.data[DOMAIN][config_entry_id].get(DATA_CLIENT)
    if not client:
        connection.send_error(msg["id"], "not_found", "Client not found")
        return

    try:
        policies = await client.network.get_group_policies(network_id)
        connection.send_result(msg["id"], policies)
    except Exception as e:
        _LOGGER.error("Error fetching group policies: %s", e)
        connection.send_error(msg["id"], "fetch_error", str(e))
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
