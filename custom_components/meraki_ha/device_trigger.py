"""Provides device triggers for Meraki."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_MERAKI_WEBHOOK_ALERT

TRIGGER_TYPE = "meraki_alert"

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): TRIGGER_TYPE,
    }
)


def _get_meraki_serial(device: dr.DeviceEntry) -> str | None:
    """Extract Meraki serial from device identifiers."""
    for identifier in device.identifiers:
        if identifier[0] == DOMAIN:
            return identifier[1]
    return None


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for Meraki devices."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)

    if device is None or _get_meraki_serial(device) is None:
        return []

    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: TRIGGER_TYPE,
        }
    ]


def _is_trigger_match(data: dict[str, Any], serial: str) -> bool:
    """Check if event data matches the device serial."""
    if data.get("deviceSerial") == serial:
        return True

    if serial.startswith("network_") and data.get("networkId") == serial[8:]:
        return True

    return False


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    device_registry = dr.async_get(hass)
    device_id = config[CONF_DEVICE_ID]
    device = device_registry.async_get(device_id)

    if device is None:
        return lambda: None

    serial = _get_meraki_serial(device)
    if not serial:
        return lambda: None

    @callback
    def handle_event(event: Event) -> None:
        data = event.data

        if _is_trigger_match(data, serial):
            hass.async_run_job(
                action,
                {
                    "trigger": {
                        **config,
                        "description": (
                            f"Meraki Alert: {data.get('alertType', 'Unknown')}"
                        ),
                        "payload": data,
                    }
                },
                event.context,
            )

    return hass.bus.async_listen(EVENT_MERAKI_WEBHOOK_ALERT, handle_event)
