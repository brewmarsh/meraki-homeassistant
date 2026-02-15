"""Provides device triggers for Meraki."""
from __future__ import annotations

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


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for Meraki devices."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)

    if device is None:
        return []

    # Check if this device belongs to our domain
    is_meraki_device = False
    for identifier in device.identifiers:
        if identifier[0] == DOMAIN:
            is_meraki_device = True
            break

    if not is_meraki_device:
        return []

    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: TRIGGER_TYPE,
        }
    ]


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

    # Extract serial from identifiers
    serial = None
    for identifier in device.identifiers:
        if identifier[0] == DOMAIN:
            serial = identifier[1]
            break

    if not serial:
        return lambda: None

    @callback
    def handle_event(event: Event) -> None:
        data = event.data
        match = False

        # Check for device serial match
        if "deviceSerial" in data and data["deviceSerial"] == serial:
            match = True

        # Check for network ID match if the device is a Network device
        elif serial.startswith("network_") and "networkId" in data:
            network_id = serial[8:]  # remove "network_"
            if data["networkId"] == network_id:
                match = True

        if match:
            hass.async_run_job(
                action,
                {
                    "trigger": {
                        **config,
                        "description": f"Meraki Alert: {data.get('alertType', 'Unknown')}",
                        "payload": data,
                    }
                },
                event.context,
            )

    return hass.bus.async_listen(EVENT_MERAKI_WEBHOOK_ALERT, handle_event)
