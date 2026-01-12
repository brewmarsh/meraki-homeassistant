"""Handles device-related webhook alerts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_handle_device_alert(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict[str, Any],
) -> None:
    """Handle device status alerts (up/down/rebooted).

    Args:
    ----
        coordinator: The Meraki data coordinator.
        alert_type: The type of alert (e.g., "APs came up").
        data: The alert data from the webhook.

    """
    _LOGGER.debug("Handling device alert: %s", alert_type)
    serial = data.get("deviceSerial")
    if not serial:
        _LOGGER.warning("Device alert missing 'deviceSerial': %s", data)
        return

    is_up = "came up" in alert_type or "came online" in alert_type
    is_down = "went down" in alert_type or "went offline" in alert_type
    is_rebooted = "rebooted" in alert_type

    if is_up or is_down or is_rebooted:
        is_online = is_up or is_rebooted
        status = "online" if is_online else "offline"
        _LOGGER.info(
            "Device %s changed status to %s via webhook (%s)",
            serial,
            status,
            alert_type,
        )
        coordinator._update_device_status_immediate(serial, is_online)
        coordinator.async_update_listeners()

        coordinator.hass.async_create_task(
            coordinator._targeted_device_refresh(serial, delay=5)
        )
