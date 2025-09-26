"""Schema definitions for the Meraki Home Assistant integration."""

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_IGNORED_NETWORKS,
    DEFAULT_IGNORED_NETWORKS,
    CONF_ENABLE_WEB_UI,
    DEFAULT_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    DEFAULT_WEB_UI_PORT,
    CONF_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VPN,
    DEFAULT_ENABLE_VPN,
    CONF_AUTO_RTSP,
    DEFAULT_AUTO_RTSP,
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)

MENU_SCHEMA = vol.Schema(
    {
        vol.Optional("next_step"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=["general", "advanced", "features"],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        )
    }
)

FEATURES_SCHEMA = vol.Schema(
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
        vol.Required(CONF_ENABLE_VPN, default=DEFAULT_ENABLE_VPN): selector.BooleanSelector(),
        vol.Required(CONF_AUTO_RTSP, default=DEFAULT_AUTO_RTSP): selector.BooleanSelector(),
    }
)

GENERAL_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=30, max=86400, step=1, mode=selector.NumberSelectorMode.SLIDER
            )
        ),
        vol.Required(CONF_ENABLE_DEVICE_TRACKER, default=True): selector.BooleanSelector(),
    }
)

ADVANCED_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_IGNORED_NETWORKS, default=DEFAULT_IGNORED_NETWORKS
        ): selector.TextSelector(),
        vol.Required(CONF_ENABLE_WEB_UI, default=DEFAULT_ENABLE_WEB_UI): selector.BooleanSelector(),
        vol.Required(CONF_WEB_UI_PORT, default=DEFAULT_WEB_UI_PORT): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1024, max=65535, step=1, mode=selector.NumberSelectorMode.BOX
            )
        ),
    }
)
