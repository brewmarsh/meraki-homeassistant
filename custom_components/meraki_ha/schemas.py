"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_CAMERA_LINK_INTEGRATION,
    CONF_CAMERA_SNAPSHOT_INTERVAL,
    CONF_DASHBOARD_DEVICE_TYPE_FILTER,
    CONF_DASHBOARD_STATUS_FILTER,
    CONF_DASHBOARD_VIEW_MODE,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DASHBOARD_VIEW_MODE_NETWORK,
    DASHBOARD_VIEW_MODE_TYPE,
    DEFAULT_CAMERA_LINK_INTEGRATION,
    DEFAULT_CAMERA_SNAPSHOT_INTERVAL,
    DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER,
    DEFAULT_DASHBOARD_STATUS_FILTER,
    DEFAULT_DASHBOARD_VIEW_MODE,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
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
        vol.Required(
            CONF_CAMERA_SNAPSHOT_INTERVAL, default=DEFAULT_CAMERA_SNAPSHOT_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                max=3600,
                step=10,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        # Dashboard display settings
        vol.Required(
            CONF_DASHBOARD_VIEW_MODE, default=DEFAULT_DASHBOARD_VIEW_MODE
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": DASHBOARD_VIEW_MODE_NETWORK, "label": "By Network"},
                    {"value": DASHBOARD_VIEW_MODE_TYPE, "label": "By Device Type"},
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_DASHBOARD_DEVICE_TYPE_FILTER,
            default=DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER,
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "all", "label": "All Types"},
                    {"value": "switch", "label": "Switches"},
                    {"value": "camera", "label": "Cameras"},
                    {"value": "wireless", "label": "Wireless APs"},
                    {"value": "sensor", "label": "Sensors"},
                    {"value": "appliance", "label": "Appliances"},
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_DASHBOARD_STATUS_FILTER, default=DEFAULT_DASHBOARD_STATUS_FILTER
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "all", "label": "All Statuses"},
                    {"value": "online", "label": "Online"},
                    {"value": "offline", "label": "Offline"},
                    {"value": "alerting", "label": "Alerting"},
                    {"value": "dormant", "label": "Dormant"},
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional(
            CONF_CAMERA_LINK_INTEGRATION, default=DEFAULT_CAMERA_LINK_INTEGRATION
        ): selector.TextSelector(
            selector.TextSelectorConfig(
                type=selector.TextSelectorType.TEXT,
            )
        ),
    }
)
