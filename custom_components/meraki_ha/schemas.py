"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_ORG_SENSORS,
    CONF_ENABLE_PORT_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_VLAN_SENSORS,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_CAMERA_ENTITIES,
    DEFAULT_ENABLE_DEVICE_SENSORS,
    DEFAULT_ENABLE_DEVICE_STATUS,
    DEFAULT_ENABLE_NETWORK_SENSORS,
    DEFAULT_ENABLE_ORG_SENSORS,
    DEFAULT_ENABLE_PORT_SENSORS,
    DEFAULT_ENABLE_SSID_SENSORS,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLE_VLAN_SENSORS,
    DEFAULT_ENABLED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=30, max=86400, step=1, mode=selector.NumberSelectorMode.SLIDER
            )
        ),
        vol.Required(
            CONF_ENABLE_DEVICE_TRACKER, default=True
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_VLAN_MANAGEMENT, default=DEFAULT_ENABLE_VLAN_MANAGEMENT
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_DEVICE_STATUS, default=DEFAULT_ENABLE_DEVICE_STATUS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_ORG_SENSORS, default=DEFAULT_ENABLE_ORG_SENSORS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_CAMERA_ENTITIES, default=DEFAULT_ENABLE_CAMERA_ENTITIES
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_DEVICE_SENSORS, default=DEFAULT_ENABLE_DEVICE_SENSORS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_NETWORK_SENSORS, default=DEFAULT_ENABLE_NETWORK_SENSORS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_VLAN_SENSORS, default=DEFAULT_ENABLE_VLAN_SENSORS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_PORT_SENSORS, default=DEFAULT_ENABLE_PORT_SENSORS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_SSID_SENSORS, default=DEFAULT_ENABLE_SSID_SENSORS
        ): selector.BooleanSelector(),
        vol.Optional(
            CONF_ENABLED_NETWORKS, default=DEFAULT_ENABLED_NETWORKS
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[],
                multiple=True,
                custom_value=False,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)
