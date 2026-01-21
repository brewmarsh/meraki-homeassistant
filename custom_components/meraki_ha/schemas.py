"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_IGNORED_NETWORKS,
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
            CONF_ENABLE_VPN_MANAGEMENT, default=DEFAULT_ENABLE_VPN_MANAGEMENT
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_FIREWALL_RULES, default=DEFAULT_ENABLE_FIREWALL_RULES
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_TRAFFIC_SHAPING, default=DEFAULT_ENABLE_TRAFFIC_SHAPING
        ): selector.BooleanSelector(),
        vol.Optional(
            CONF_IGNORED_NETWORKS, default=DEFAULT_IGNORED_NETWORKS
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[],
                multiple=True,
                custom_value=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)
