"""Config flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import callback

from .authentication import validate_meraki_credentials
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .const import (
    CONF_AUTO_ENABLE_RTSP,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_DEVICE_NAME_FORMAT,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_WEBHOOK_URL,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_IGNORED_NETWORKS,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEBHOOK_URL,
    DEFAULT_ENABLE_WEB_UI,
    DEFAULT_WEB_UI_PORT,
    DEFAULT_HIDE_UNCONFIGURED_SSIDS,
    DEFAULT_IGNORED_NETWORKS,
    DEVICE_NAME_FORMAT_OPTIONS,
    DOMAIN,
)
from .options_flow import MerakiOptionsFlowHandler

_LOGGER = logging.getLogger(__name__)


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the config flow."""
        self.data: Dict[str, Any] = {}
        self.options: Dict[str, Any] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                validation_result = await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY],
                    user_input[CONF_MERAKI_ORG_ID],
                )
                self.data[CONF_MERAKI_API_KEY] = user_input[CONF_MERAKI_API_KEY]
                self.data[CONF_MERAKI_ORG_ID] = user_input[CONF_MERAKI_ORG_ID]
                self.data["org_name"] = validation_result.get(
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
                )

                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                self._abort_if_unique_id_configured()

                return await self.async_step_general()

            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except data_entry_flow.AbortFlow as e:
                raise e
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MERAKI_API_KEY): str,
                    vol.Required(CONF_MERAKI_ORG_ID): str,
                }
            ),
            errors=errors,
        )

    async def async_step_general(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the general settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_features()

        return self.async_show_form(
            step_id="general",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): int,
                    vol.Optional(
                        CONF_DEVICE_NAME_FORMAT, default=DEFAULT_DEVICE_NAME_FORMAT
                    ): vol.In(DEVICE_NAME_FORMAT_OPTIONS),
                }
            ),
        )

    async def async_step_features(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the features settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_advanced()

        return self.async_show_form(
            step_id="features",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_AUTO_ENABLE_RTSP, default=False): bool,
                    vol.Optional(CONF_USE_LAN_IP_FOR_RTSP, default=False): bool,
                    vol.Optional(CONF_ENABLE_DEVICE_TRACKER, default=True): bool,
                    vol.Optional(
                        CONF_ENABLE_WEB_UI, default=DEFAULT_ENABLE_WEB_UI
                    ): bool,
                    vol.Optional(CONF_WEB_UI_PORT, default=DEFAULT_WEB_UI_PORT): int,
                    vol.Optional(
                        CONF_HIDE_UNCONFIGURED_SSIDS,
                        default=DEFAULT_HIDE_UNCONFIGURED_SSIDS,
                    ): bool,
                }
            ),
        )

    async def async_step_advanced(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the advanced settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.data["org_name"], data=self.data, options=self.options
            )

        return self.async_show_form(
            step_id="advanced",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_WEBHOOK_URL, default=DEFAULT_WEBHOOK_URL): str,
                    vol.Optional(
                        CONF_IGNORED_NETWORKS, default=DEFAULT_IGNORED_NETWORKS
                    ): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)
