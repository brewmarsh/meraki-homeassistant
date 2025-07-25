"""Schema definitions for the Meraki Home Assistant integration."""

import voluptuous as vol
from homeassistant.helpers import selector
from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
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

RECONFIGURE_SCHEMA = vol.Schema(
    {
        vol.Required(
            "scan_interval",
            default=DEFAULT_SCAN_INTERVAL,
        ): int,
        vol.Optional(
            "device_name_format",
            default="omitted",
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "prefix", "label": "Prefix"},
                    {"value": "suffix", "label": "Suffix"},
                    {"value": "omitted", "label": "Omitted"},
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)
