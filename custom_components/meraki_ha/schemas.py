"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_ORG_SENSORS,
    CONF_ENABLE_PORT_SENSORS,
    CONF_ENABLE_SSID_SENSORS,
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
    DEFAULT_ENABLE_DEVICE_TRACKER,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_NETWORK_SENSORS,
    DEFAULT_ENABLE_ORG_SENSORS,
    DEFAULT_ENABLE_PORT_SENSORS,
    DEFAULT_ENABLE_SSID_SENSORS,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLE_VLAN_SENSORS,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_ENABLED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
)
from homeassistant.helpers import selector

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
    }
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
    }
)


def get_org_selection_schema(orgs: list[dict[str, Any]]) -> vol.Schema:
    """Return the organization selection schema."""
    return vol.Schema(
        {
            vol.Required(CONF_MERAKI_ORG_ID): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(label=org["name"], value=org["id"])
                        for org in orgs
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


def get_network_selection_schema(networks: list[dict[str, Any]]) -> vol.Schema:
    """Return the network selection schema."""
    return vol.Schema(
        {
            vol.Required(CONF_ENABLED_NETWORKS): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(label=net["name"], value=net["id"])
                        for net in networks
                    ],
                    multiple=True,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


def get_options_schema_general(options: dict[str, Any]) -> vol.Schema:
    """Return the general options schema with defaults."""
    return vol.Schema(
        {
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
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
                CONF_ENABLED_NETWORKS,
                default=options.get(CONF_ENABLED_NETWORKS, DEFAULT_ENABLED_NETWORKS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[],
                    multiple=True,
                    custom_value=True,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_ENABLE_DEVICE_TRACKER,
                default=options.get(
                    CONF_ENABLE_DEVICE_TRACKER, DEFAULT_ENABLE_DEVICE_TRACKER
                ),
            ): selector.BooleanSelector(),
        }
    )


def get_options_schema_sensors(options: dict[str, Any]) -> vol.Schema:
    """Return the sensors options schema with defaults."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ENABLE_DEVICE_STATUS,
                default=options.get(
                    CONF_ENABLE_DEVICE_STATUS, DEFAULT_ENABLE_DEVICE_STATUS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_ORG_SENSORS,
                default=options.get(
                    CONF_ENABLE_ORG_SENSORS, DEFAULT_ENABLE_ORG_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_DEVICE_SENSORS,
                default=options.get(
                    CONF_ENABLE_DEVICE_SENSORS, DEFAULT_ENABLE_DEVICE_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_NETWORK_SENSORS,
                default=options.get(
                    CONF_ENABLE_NETWORK_SENSORS, DEFAULT_ENABLE_NETWORK_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_VLAN_SENSORS,
                default=options.get(
                    CONF_ENABLE_VLAN_SENSORS, DEFAULT_ENABLE_VLAN_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_PORT_SENSORS,
                default=options.get(
                    CONF_ENABLE_PORT_SENSORS, DEFAULT_ENABLE_PORT_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_SSID_SENSORS,
                default=options.get(
                    CONF_ENABLE_SSID_SENSORS, DEFAULT_ENABLE_SSID_SENSORS
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_CLIENT_STATUS_SENSORS,
                default=options.get(
                    CONF_ENABLE_CLIENT_STATUS_SENSORS,
                    DEFAULT_ENABLE_CLIENT_STATUS_SENSORS,
                ),
            ): selector.BooleanSelector(),
        }
    )


def get_options_schema_cameras(options: dict[str, Any]) -> vol.Schema:
    """Return the cameras options schema with defaults."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ENABLE_CAMERA_ENTITIES,
                default=options.get(
                    CONF_ENABLE_CAMERA_ENTITIES, DEFAULT_ENABLE_CAMERA_ENTITIES
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_CAMERA_SENSE,
                default=options.get(
                    CONF_ENABLE_CAMERA_SENSE, DEFAULT_ENABLE_CAMERA_SENSE
                ),
            ): selector.BooleanSelector(),
        }
    )


def get_options_schema_advanced(options: dict[str, Any]) -> vol.Schema:
    """Return the advanced options schema with defaults."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ENABLE_VLAN_MANAGEMENT,
                default=options.get(
                    CONF_ENABLE_VLAN_MANAGEMENT, DEFAULT_ENABLE_VLAN_MANAGEMENT
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_TRAFFIC_SHAPING,
                default=options.get(
                    CONF_ENABLE_TRAFFIC_SHAPING, DEFAULT_ENABLE_TRAFFIC_SHAPING
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_FIREWALL_RULES,
                default=options.get(
                    CONF_ENABLE_FIREWALL_RULES, DEFAULT_ENABLE_FIREWALL_RULES
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ENABLE_VPN_MANAGEMENT,
                default=options.get(
                    CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT
                ),
            ): selector.BooleanSelector(),
        }
    )


OPTIONS_SCHEMA_GENERAL = get_options_schema_general({})
OPTIONS_SCHEMA_SENSORS = get_options_schema_sensors({})
OPTIONS_SCHEMA_CAMERAS = get_options_schema_cameras({})
OPTIONS_SCHEMA_ADVANCED = get_options_schema_advanced({})

OPTIONS_SCHEMA = (
    OPTIONS_SCHEMA_GENERAL.extend(OPTIONS_SCHEMA_SENSORS.schema)
    .extend(OPTIONS_SCHEMA_CAMERAS.schema)
    .extend(OPTIONS_SCHEMA_ADVANCED.schema)
)
