"""Options flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
import voluptuous as vol

from .const import (
    CONF_AUTO_ENABLE_RTSP,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_DEVICE_NAME_FORMAT,
    CONF_WEBHOOK_URL,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_IGNORED_NETWORKS,
    CONF_USE_STALE_DATA,
    CONF_STALE_DATA_THRESHOLD,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEBHOOK_URL,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_WEB_UI_PORT,
    DEFAULT_HIDE_UNCONFIGURED_SSIDS,
    DEFAULT_IGNORED_NETWORKS,
    DEVICE_NAME_FORMAT_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the general settings step."""
        if user_input is not None:
            # We don't want to save the display-only field
            user_input.pop("config_entry_id_display", None)
            self.options.update(user_input)
            return await self.async_step_features()

        # The config_entry is available as self.config_entry in an options flow
        return self.async_show_form(
            step_id="init",
            description_placeholders={"config_entry_id": self.config_entry.entry_id},
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                    vol.Optional(
                        CONF_DEVICE_NAME_FORMAT,
                        default=self.options.get(
                            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
                        ),
                    ): vol.In(DEVICE_NAME_FORMAT_OPTIONS),
                }
            ),
        )

    async def async_step_features(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the features settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_advanced()

        port = self.options.get(CONF_WEB_UI_PORT, DEFAULT_WEB_UI_PORT)
        host = self.hass.config.api.host if self.hass.config.api else "localhost"
        web_ui_url = f"http://{host}:{port}"

        return self.async_show_form(
            step_id="features",
            description_placeholders={"web_ui_url": web_ui_url},
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_AUTO_ENABLE_RTSP,
                        default=self.options.get(CONF_AUTO_ENABLE_RTSP, False),
                    ): bool,
                    vol.Optional(
                        CONF_USE_LAN_IP_FOR_RTSP,
                        default=self.options.get(CONF_USE_LAN_IP_FOR_RTSP, False),
                    ): bool,
                    vol.Optional(
                        CONF_ENABLE_DEVICE_TRACKER,
                        default=self.options.get(CONF_ENABLE_DEVICE_TRACKER, True),
                    ): bool,
                    vol.Optional(
                        CONF_ENABLE_WEB_UI,
                        default=self.options.get(
                            CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_WEB_UI_PORT,
                        default=port,
                    ): int,
                    vol.Optional(
                        CONF_HIDE_UNCONFIGURED_SSIDS,
                        default=self.options.get(
                            CONF_HIDE_UNCONFIGURED_SSIDS,
                            DEFAULT_HIDE_UNCONFIGURED_SSIDS,
                        ),
                    ): bool,
                }
            ),
        )

    async def async_step_advanced(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the advanced settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="advanced",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_WEBHOOK_URL,
                        default=self.options.get(CONF_WEBHOOK_URL, DEFAULT_WEBHOOK_URL),
                    ): str,
                    vol.Optional(
                        CONF_IGNORED_NETWORKS,
                        default=self.options.get(
                            CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
                        ),
                    ): str,
                    vol.Optional(
                        CONF_USE_STALE_DATA,
                        default=self.options.get(CONF_USE_STALE_DATA, True),
                    ): bool,
                    vol.Optional(
                        CONF_STALE_DATA_THRESHOLD,
                        default=self.options.get(CONF_STALE_DATA_THRESHOLD, 30),
                    ): int,
                }
            ),
        )
