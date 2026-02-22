"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const_conf import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_ORG_SENSORS,
    CONF_ENABLE_PORT_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_VLAN_SENSORS,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_CAMERA_ENTITIES,
    DEFAULT_ENABLE_CAMERA_SENSE,
    DEFAULT_ENABLE_CLIENT_STATUS_SENSORS,
    DEFAULT_ENABLE_DEVICE_SENSORS,
    DEFAULT_ENABLE_DEVICE_STATUS,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_NETWORK_SENSORS,
    DEFAULT_ENABLE_ORG_SENSORS,
    DEFAULT_ENABLE_PORT_SENSORS,
    DEFAULT_ENABLE_SSID_SENSORS,
    DEFAULT_ENABLE_CLIENT_STATUS_SENSORS,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLE_VLAN_SENSORS,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
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

OPTIONS_SCHEMA_GENERAL = vol.Schema(
    {
        vol.Required(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(label="Fast (60s)", value="60"),
                    selector.SelectOptionDict(label="Normal (300s)", value="300"),
                    selector.SelectOptionDict(label="Slow (900s)", value="900"),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional(
            CONF_ENABLED_NETWORKS, default=DEFAULT_ENABLED_NETWORKS
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[],
                multiple=True,
                custom_value=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_ENABLE_DEVICE_TRACKER, default=True
        ): selector.BooleanSelector(),
    }
)

OPTIONS_SCHEMA_SENSORS = vol.Schema(
    {
        vol.Required(
            CONF_ENABLE_DEVICE_STATUS, default=DEFAULT_ENABLE_DEVICE_STATUS
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_ORG_SENSORS, default=DEFAULT_ENABLE_ORG_SENSORS
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
        vol.Required(
            CONF_ENABLE_CLIENT_STATUS_SENSORS,
            default=DEFAULT_ENABLE_CLIENT_STATUS_SENSORS,
        ): selector.BooleanSelector(),
    }
)

OPTIONS_SCHEMA_CAMERAS = vol.Schema(
    {
        vol.Required(
            CONF_ENABLE_CAMERA_ENTITIES, default=DEFAULT_ENABLE_CAMERA_ENTITIES
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_CAMERA_SENSE, default=DEFAULT_ENABLE_CAMERA_SENSE
        ): selector.BooleanSelector(),
    }
)

OPTIONS_SCHEMA_ADVANCED = vol.Schema(
    {
        vol.Required(
            CONF_ENABLE_VLAN_MANAGEMENT, default=DEFAULT_ENABLE_VLAN_MANAGEMENT
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_FIREWALL_RULES, default=DEFAULT_ENABLE_FIREWALL_RULES
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_TRAFFIC_SHAPING, default=DEFAULT_ENABLE_TRAFFIC_SHAPING
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_VPN_MANAGEMENT, default=DEFAULT_ENABLE_VPN_MANAGEMENT
        ): selector.BooleanSelector(),
    }
)

OPTIONS_SCHEMA = vol.Schema(
    {
        **OPTIONS_SCHEMA_GENERAL.schema,
        **OPTIONS_SCHEMA_SENSORS.schema,
        **OPTIONS_SCHEMA_CAMERAS.schema,
        **OPTIONS_SCHEMA_ADVANCED.schema,
    }
)
