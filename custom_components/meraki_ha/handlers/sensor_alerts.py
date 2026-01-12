"""Handles sensor-related webhook alerts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..const import DOMAIN
from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_handle_sensor_alert(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict[str, Any],
) -> None:
    """Handle MT sensor alerts.

    Handles environmental sensor threshold alerts:
    - Temperature threshold exceeded
    - Humidity threshold exceeded
    - Water detected
    - Door opened/closed
    - Power outage detected

    These alerts fire Home Assistant events for automations and
    trigger a device refresh to get the latest sensor readings.

    Args:
    ----
        coordinator: The Meraki data coordinator.
        alert_type: The type of alert.
        data: The alert data from the webhook.

    """
    _LOGGER.info("Sensor alert received: %s", alert_type)

    serial = data.get("deviceSerial")
    if not serial:
        _LOGGER.warning("Sensor alert missing 'deviceSerial': %s", data)
        return

    alert_data = data.get("alertData", {})
    alert_lower = alert_type.lower()
    network_name = data.get("networkName", "Unknown Network")
    device_name = data.get("deviceName", serial)

    # Determine the sensor alert category
    if "temperature" in alert_lower:
        event_type = "temperature_threshold"
        current_value = alert_data.get("temperature") or alert_data.get("value")
        threshold = alert_data.get("threshold")
        _LOGGER.info(
            "Temperature threshold alert for %s: %s (threshold: %s)",
            device_name,
            current_value,
            threshold,
        )
    elif "humidity" in alert_lower:
        event_type = "humidity_threshold"
        current_value = alert_data.get("humidity") or alert_data.get("value")
        threshold = alert_data.get("threshold")
        _LOGGER.info(
            "Humidity threshold alert for %s: %s (threshold: %s)",
            device_name,
            current_value,
            threshold,
        )
    elif "water" in alert_lower:
        event_type = "water_detected"
        current_value = True
        threshold = None
        _LOGGER.warning("Water detected by sensor %s!", device_name)
    elif "door" in alert_lower:
        event_type = "door_change"
        is_open = alert_data.get("open", alert_data.get("state") == "open")
        current_value = "open" if is_open else "closed"
        threshold = None
        _LOGGER.info("Door sensor %s: %s", device_name, current_value)
    elif "power" in alert_lower:
        event_type = "power_outage"
        current_value = alert_data.get("powerStatus", "outage")
        threshold = None
        _LOGGER.warning("Power outage detected by sensor %s!", device_name)
    else:
        event_type = "sensor_alert"
        current_value = alert_data.get("value")
        threshold = alert_data.get("threshold")
        _LOGGER.info("Sensor alert for %s: %s", device_name, alert_type)

    # Fire Home Assistant event for automations
    event_data = {
        "alert_type": alert_type,
        "event_type": event_type,
        "device_serial": serial,
        "device_name": device_name,
        "network_name": network_name,
        "value": current_value,
        "threshold": threshold,
        "occurred_at": data.get("occurredAt"),
        "alert_data": alert_data,
    }

    coordinator.hass.bus.async_fire(f"{DOMAIN}_sensor_alert", event_data)
    _LOGGER.debug("Fired sensor alert event: %s", event_data)

    # Trigger a debounced device refresh to get latest readings
    key = f"device:{serial}"
    coordinator.schedule_debounced_refresh(
        key,
        coordinator._targeted_device_refresh(serial, delay=2),
    )
