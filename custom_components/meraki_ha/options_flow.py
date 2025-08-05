"""Options flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
import voluptuous as vol

from .const import (
    CONF_AUTO_ENABLE_RTSP,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_DEVICE_NAME_FORMAT,
    CONF_WEBHOOK_URL,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEBHOOK_URL,
    DEVICE_NAME_FORMAT_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the options flow initialization."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL,
                            self.config_entry.data.get(
                                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                            ),
                        ),
                    ): int,
                    vol.Optional(
                        CONF_DEVICE_NAME_FORMAT,
                        default=self.config_entry.options.get(
                            CONF_DEVICE_NAME_FORMAT,
                            self.config_entry.data.get(
                                CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
                            ),
                        ),
                    ): vol.In(DEVICE_NAME_FORMAT_OPTIONS),
                    vol.Optional(
                        CONF_AUTO_ENABLE_RTSP,
                        default=self.config_entry.options.get(
                            CONF_AUTO_ENABLE_RTSP,
                            self.config_entry.data.get(CONF_AUTO_ENABLE_RTSP, False),
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_USE_LAN_IP_FOR_RTSP,
                        default=self.config_entry.options.get(
                            CONF_USE_LAN_IP_FOR_RTSP,
                            self.config_entry.data.get(CONF_USE_LAN_IP_FOR_RTSP, False),
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_WEBHOOK_URL,
                        default=self.config_entry.options.get(
                            CONF_WEBHOOK_URL,
                            self.config_entry.data.get(
                                CONF_WEBHOOK_URL, DEFAULT_WEBHOOK_URL
                            ),
                        ),
                    ): str,
                }
            ),
        )
