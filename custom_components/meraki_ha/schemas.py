"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_VLAN_MANAGEMENT,
<<<<<<< HEAD
    CONF_ENABLED_NETWORKS,
=======
    CONF_IGNORED_NETWORKS,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
<<<<<<< HEAD
    DEFAULT_ENABLED_NETWORKS,
=======
    DEFAULT_IGNORED_NETWORKS,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
            CONF_ENABLED_NETWORKS, default=DEFAULT_ENABLED_NETWORKS
=======
            CONF_IGNORED_NETWORKS, default=DEFAULT_IGNORED_NETWORKS
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[],
                multiple=True,
<<<<<<< HEAD
                custom_value=False,
=======
                custom_value=True,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)
