"""Handles client-related webhook alerts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..const import DOMAIN
from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_handle_client_alert(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict[str, Any],
) -> None:
    """Handle client-related alerts.

    Handles:
    - Client connectivity changed
    - New client connected
    - Client blocked

    Args:
    ----
        coordinator: The Meraki data coordinator.
        alert_type: The type of alert.
        data: The alert data from the webhook.

    """
    _LOGGER.debug("Handling client alert: %s", alert_type)
    alert_data = data.get("alertData", {})
    alert_lower = alert_type.lower()

    # Extract client MAC from various possible locations
    client_mac = (
        alert_data.get("mac") or alert_data.get("clientMac") or data.get("clientMac")
    )

    network_id = data.get("networkId")
    network_name = data.get("networkName", "Unknown Network")

    # Handle "New client connected"
    if "new client" in alert_lower:
        if not client_mac:
            _LOGGER.warning("New client alert missing MAC: %s", data)
            return

        client_name = alert_data.get("name", "Unknown")
        _LOGGER.info(
            "New client connected: %s (%s) on network %s",
            client_name,
            client_mac,
            network_name,
        )

        # Fire event for automations
        coordinator.hass.bus.async_fire(
            f"{DOMAIN}_new_client",
            {
                "mac": client_mac,
                "name": client_name,
                "network_id": network_id,
                "network_name": network_name,
                "alert_data": alert_data,
            },
        )

        # Trigger auto-sync if enabled
        await _maybe_auto_sync_client(coordinator, client_mac, network_id)

        # Refresh client data with debouncing
        if network_id:
            key = f"client:{network_id}:{client_mac}"
            coordinator.schedule_debounced_refresh(
                key,
                coordinator._targeted_client_refresh(
                    network_id=network_id,
                    client_mac=client_mac,
                    delay=5,
                ),
            )
        return

    # Handle "Client blocked"
    if "blocked" in alert_lower:
        if not client_mac:
            _LOGGER.warning("Client blocked alert missing MAC: %s", data)
            return

        _LOGGER.info(
            "Client %s was blocked on network %s",
            client_mac,
            network_name,
        )

        # Fire event for automations
        coordinator.hass.bus.async_fire(
            f"{DOMAIN}_client_blocked",
            {
                "mac": client_mac,
                "network_id": network_id,
                "network_name": network_name,
                "alert_data": alert_data,
            },
        )

        # Update client status to offline/blocked
        coordinator._update_client_status_immediate(client_mac, False)
        coordinator.async_update_listeners()
        return

    # Handle "Client connectivity changed" (original behavior)
    if not client_mac:
        _LOGGER.warning("Client alert missing 'mac': %s", data)
        return

    is_connected = alert_data.get("connected")
    if is_connected is None:
        # Try to infer from alert type
        if "disconnect" in alert_lower or "offline" in alert_lower:
            is_connected = False
        elif "connect" in alert_lower or "online" in alert_lower:
            is_connected = True
        else:
            _LOGGER.warning("Client alert missing 'connected' status: %s", data)
            return

    status = "Online" if is_connected else "Offline"
    _LOGGER.info(
        "Client %s changed status to %s via webhook (%s)",
        client_mac,
        status,
        alert_type,
    )
    coordinator._update_client_status_immediate(client_mac, is_connected)
    coordinator.async_update_listeners()

    if network_id:
        key = f"client:{network_id}:{client_mac}"
        coordinator.schedule_debounced_refresh(
            key,
            coordinator._targeted_client_refresh(
                network_id=network_id,
                client_mac=client_mac,
                delay=5,
            ),
        )


async def _maybe_auto_sync_client(
    coordinator: MerakiDataCoordinator,
    client_mac: str,
    network_id: str | None,
) -> None:
    """Sync client name to Meraki if auto-sync is enabled."""
    from ..const import CONF_SYNC_ON_NEW_CLIENT
    from ..helpers.sync_helper import build_client_description

    if not coordinator.config_entry:
        return

    auto_sync_enabled = coordinator.config_entry.options.get(
        CONF_SYNC_ON_NEW_CLIENT, False
    )
    if not auto_sync_enabled:
        return

    if not network_id:
        return

    # Get the HA device name for this MAC
    description = build_client_description(coordinator.hass, client_mac)
    if not description:
        _LOGGER.debug("No HA device found for MAC %s, skipping auto-sync", client_mac)
        return

    try:
        await coordinator.api.network.provision_network_clients(
            network_id,
            [{"mac": client_mac, "name": description}],
        )
        _LOGGER.info(
            "Auto-synced client %s with name '%s' to Meraki",
            client_mac,
            description,
        )
    except Exception as e:
        _LOGGER.warning("Failed to auto-sync client %s: %s", client_mac, e)
