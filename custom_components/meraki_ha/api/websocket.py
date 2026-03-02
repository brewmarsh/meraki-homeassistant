"""WebSocket API for Meraki HA."""

from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import async_get_integration

from ..const import DOMAIN, DATA_CLIENT
from ..helpers.serialization import to_serializable

_LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..core.api.client import MerakiAPIClient
    from ..services.camera_service import CameraService
    from ..core.timed_access_manager import TimedAccessManager


@callback
def async_setup_websocket_api(hass: HomeAssistant) -> None:
    """Set up the WebSocket API."""
    # Register the command to get Meraki config
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_config",
        ws_get_config,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/get_config",
                vol.Required("config_entry_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
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
    # Register the command to fetch network events
    websocket_api.async_register_command(
        hass,
        "meraki_ha/get_network_events",
        ws_get_network_events,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/get_network_events",
                vol.Required("config_entry_id"): str,
                vol.Required("network_id"): str,
                vol.Optional("per_page"): int,
                vol.Optional("product_type"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to update options
    websocket_api.async_register_command(
        hass,
        "meraki_ha/update_options",
        ws_update_options,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/update_options",
                vol.Required("config_entry_id"): str,
                vol.Required("options"): dict,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to update enabled networks
    websocket_api.async_register_command(
        hass,
        "meraki_ha/update_enabled_networks",
        ws_update_enabled_networks,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/update_enabled_networks",
                vol.Required("config_entry_id"): str,
                vol.Required("enabled_networks"): [str],
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to get timed access keys
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/get_keys",
        ws_timed_access_get_keys,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/timed_access/get_keys",
                vol.Required("config_entry_id"): str,
                vol.Optional("network_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to get group policies
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/get_policies",
        ws_timed_access_get_policies,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/timed_access/get_policies",
                vol.Required("config_entry_id"): str,
                vol.Required("network_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to create a timed access key
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/create",
        ws_timed_access_create,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/timed_access/create",
                vol.Required("config_entry_id"): str,
                vol.Required("network_id"): str,
                vol.Required("ssid_number"): str,
                vol.Required("duration"): int,
                vol.Optional("name"): str,
                vol.Optional("passphrase"): str,
                vol.Optional("group_policy_id"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )
    # Register the command to delete a timed access key
    websocket_api.async_register_command(
        hass,
        "meraki_ha/timed_access/delete",
        ws_timed_access_delete,
        vol.Schema(
            {
                vol.Required("type"): "meraki_ha/timed_access/delete",
                vol.Required("config_entry_id"): str,
                vol.Required("identity_psk_id"): str,
                vol.Required("network_id"): str,
                vol.Required("ssid_number"): str,
            },
            extra=vol.ALLOW_EXTRA,
        ),
    )


@websocket_api.async_response
async def ws_get_config(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_config command."""
    try:
        config_entry_id = msg["config_entry_id"]

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        coordinator = hass.data[DOMAIN][config_entry_id][
            "main_coordinator"
        ]
        data = to_serializable(coordinator.data)
        connection.send_result(msg["id"], data)
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


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

        coordinator = hass.data[DOMAIN][config_entry_id][
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
    try:
        config_entry_id = msg["config_entry_id"]
        serial = msg["serial"]
        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        camera_service: CameraService = hass.data[DOMAIN][config_entry_id][
            "camera_service"
        ]
        stream_url = await camera_service.get_video_stream_url(serial)
        connection.send_result(msg["id"], {"url": stream_url})
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


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
    try:
        config_entry_id = msg["config_entry_id"]
        serial = msg["serial"]
        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        camera_service: CameraService = hass.data[DOMAIN][config_entry_id][
            "camera_service"
        ]
        snapshot_url = await camera_service.get_camera_snapshot(serial)
        connection.send_result(msg["id"], {"url": snapshot_url})
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_get_version(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_version command."""
    try:
        integration = await async_get_integration(hass, DOMAIN)
        version = str(integration.version)
        connection.send_result(msg["id"], {"version": version})
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_get_network_events(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle get_network_events command."""
    try:
        config_entry_id = msg["config_entry_id"]
        network_id = msg["network_id"]
        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        client: MerakiAPIClient = hass.data[DOMAIN][config_entry_id][DATA_CLIENT]

        params = {}
        if "per_page" in msg:
            params["per_page"] = msg["per_page"]
        if "product_type" in msg:
            params["product_type"] = msg["product_type"]

        events = await client.network.get_network_events(network_id, **params)
        connection.send_result(msg["id"], to_serializable(events))
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_update_options(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle update_options command."""
    try:
        config_entry_id = msg["config_entry_id"]
        options = msg["options"]

        entry = hass.config_entries.async_get_entry(config_entry_id)
        if not entry:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        hass.config_entries.async_update_entry(entry, options=options)
        connection.send_result(msg["id"], {"success": True})
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_update_enabled_networks(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle update_enabled_networks command."""
    try:
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
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_timed_access_get_keys(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle timed_access/get_keys command."""
    try:
        config_entry_id = msg["config_entry_id"]
        network_id = msg.get("network_id")

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        manager: TimedAccessManager = hass.data[DOMAIN][config_entry_id]["timed_access_manager"]
        keys = manager.get_keys(network_id)
        connection.send_result(msg["id"], to_serializable(keys))
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_timed_access_get_policies(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle timed_access/get_policies command."""
    try:
        config_entry_id = msg["config_entry_id"]
        network_id = msg["network_id"]

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        client: MerakiAPIClient = hass.data[DOMAIN][config_entry_id][DATA_CLIENT]
        policies = await client.network.get_group_policies(network_id)
        connection.send_result(msg["id"], to_serializable(policies))
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_timed_access_create(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle timed_access/create command."""
    try:
        config_entry_id = msg["config_entry_id"]
        network_id = msg["network_id"]
        ssid_number = msg["ssid_number"]
        duration = msg["duration"]
        name = msg.get("name")
        passphrase = msg.get("passphrase")
        group_policy_id = msg.get("group_policy_id")

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        manager: TimedAccessManager = hass.data[DOMAIN][config_entry_id]["timed_access_manager"]
        key = await manager.create_key(
            config_entry_id=config_entry_id,
            network_id=network_id,
            ssid_number=ssid_number,
            duration_minutes=duration,
            name=name,
            passphrase=passphrase,
            group_policy_id=group_policy_id,
        )
        connection.send_result(msg["id"], to_serializable(key))
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.exception("Error in ws_timed_access_create: %s", err)
        connection.send_error(msg["id"], "unknown_error", str(err))


@websocket_api.async_response
async def ws_timed_access_delete(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Handle timed_access/delete command."""
    try:
        config_entry_id = msg["config_entry_id"]
        identity_psk_id = msg["identity_psk_id"]
        network_id = msg["network_id"]
        ssid_number = msg["ssid_number"]

        if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
            connection.send_error(msg["id"], "not_found", "Config entry not found")
            return

        manager: TimedAccessManager = hass.data[DOMAIN][config_entry_id]["timed_access_manager"]
        await manager.delete_key(
            identity_psk_id=identity_psk_id,
            network_id=network_id,
            ssid_number=ssid_number,
            config_entry_id=config_entry_id,
        )
        connection.send_result(msg["id"], {"success": True})
    except Exception as err:  # pylint: disable=broad-except
        connection.send_error(msg["id"], "unknown_error", str(err))
