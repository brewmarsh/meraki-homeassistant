"""Handles security-related webhook alerts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..const import DOMAIN
from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_handle_security_alert(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict[str, Any],
) -> None:
    """Handle security alerts.

    Security alerts (rogue APs, intrusions, malware) are fired as Home Assistant
    events so users can create automations to respond to them.

    Event name: meraki_security_alert
    Event data includes:
        - alert_type: The type of security alert
        - network_id: The network where the alert occurred
        - network_name: The name of the network
        - device_serial: The device serial (if applicable)
        - occurred_at: When the alert occurred
        - alert_data: The raw alert data from Meraki

    Args:
    ----
        coordinator: The Meraki data coordinator.
        alert_type: The type of alert.
        data: The alert data from the webhook.

    """
    _LOGGER.info("Security alert received: %s", alert_type)

    # Extract useful information from the alert
    network_id = data.get("networkId")
    network_name = data.get("networkName", "Unknown Network")
    device_serial = data.get("deviceSerial")
    occurred_at = data.get("occurredAt")
    alert_data = data.get("alertData", {})

    # Fire an event so users can create automations
    event_data = {
        "alert_type": alert_type,
        "network_id": network_id,
        "network_name": network_name,
        "device_serial": device_serial,
        "occurred_at": occurred_at,
        "alert_data": alert_data,
    }

    coordinator.hass.bus.async_fire(f"{DOMAIN}_security_alert", event_data)
    _LOGGER.debug("Fired security alert event: %s", event_data)

    # If the alert is related to a specific device, trigger a refresh
    if device_serial:
        coordinator.hass.async_create_task(
            coordinator._targeted_device_refresh(device_serial, delay=5)
        )
