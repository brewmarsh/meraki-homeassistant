"""WebSocket API for Meraki HA."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from ..const import (
    CONF_CAMERA_LINK_INTEGRATION,
    CONF_DASHBOARD_DEVICE_TYPE_FILTER,
    CONF_DASHBOARD_STATUS_FILTER,
    CONF_DASHBOARD_VIEW_MODE,
    CONF_ENABLED_NETWORKS,
    CONF_SCAN_INTERVAL,
    CONF_TEMPERATURE_UNIT,
    DEFAULT_CAMERA_LINK_INTEGRATION,
    DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER,
    DEFAULT_DASHBOARD_STATUS_FILTER,
    DEFAULT_DASHBOARD_VIEW_MODE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TEMPERATURE_UNIT,
    DOMAIN,
)
from ..meraki_data_coordinator import MerakiDataCoordinator


def _build_enriched_data(
    coordinator: MerakiDataCoordinator,
    config_entry_id: str,
    hass: HomeAssistant,
) -> dict[str, Any]:
    """Build enriched data payload with coordinator data and config options."""
    config_entry = hass.config_entries.async_get_entry(config_entry_id)
    if not config_entry:
        return coordinator.data

    enabled_networks = config_entry.options.get(CONF_ENABLED_NETWORKS)
    if enabled_networks is None:
        enabled_networks = [
            n["id"] for n in coordinator.data.get("networks", []) if "id" in n
        ]

    # Use the coordinator's actual update_interval to ensure frontend is in sync
    scan_interval = (
        int(coordinator.update_interval.total_seconds())
        if coordinator.update_interval
        else config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    )
    last_updated = (
        coordinator.last_successful_update.isoformat()
        if coordinator.last_successful_update
        else None
    )

    return {
        **coordinator.data,
        "enabled_networks": enabled_networks,
        "config_entry_id": config_entry_id,
        "scan_interval": scan_interval,
        "last_updated": last_updated,
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
        "temperature_unit": config_entry.options.get(
            CONF_TEMPERATURE_UNIT, DEFAULT_TEMPERATURE_UNIT
        ),
    }


@callback
def async_setup_websocket_api(hass: HomeAssistant) -> None:
    """Set up the WebSocket API."""
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

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]

    @callback
    def async_send_update() -> None:
        """Send update to client."""
        enriched_data = _build_enriched_data(coordinator, config_entry_id, hass)
        connection.send_message(websocket_api.event_message(msg["id"], enriched_data))

    # Confirm the subscription (required by HA WebSocket protocol)
    connection.send_result(msg["id"])

    # Send initial data as an event (subscribeMessage callback only receives events)
    initial_data = _build_enriched_data(coordinator, config_entry_id, hass)
    connection.send_message(websocket_api.event_message(msg["id"], initial_data))

    # Register for updates
    cancel_subscription = coordinator.async_add_listener(async_send_update)
    connection.subscriptions[msg["id"]] = cancel_subscription
