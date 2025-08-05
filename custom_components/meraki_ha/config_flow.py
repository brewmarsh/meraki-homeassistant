"""Config flow for the Meraki Home Assistant integration.

This module defines the configuration flow for setting up and managing
the Meraki integration within Home Assistant. It handles user input for
API keys, organization IDs, and other configuration options.
"""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .authentication import validate_meraki_credentials
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .const import (
    CONF_AUTO_ENABLE_RTSP,
    CONF_DEVICE_NAME_FORMAT,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_WEBHOOK_URL,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WEBHOOK_URL,
    DEVICE_NAME_FORMAT_OPTIONS,
    DOMAIN,
)
from .options_flow import MerakiOptionsFlowHandler

_LOGGER = logging.getLogger(__name__)


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

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
                org_name = validation_result.get(
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
                )
            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                self._abort_if_unique_id_configured()
                options = {
                    CONF_SCAN_INTERVAL: user_input.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                    CONF_DEVICE_NAME_FORMAT: user_input.get(
                        CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
                    ),
                    CONF_AUTO_ENABLE_RTSP: user_input.get(
                        CONF_AUTO_ENABLE_RTSP, False
                    ),
                    CONF_WEBHOOK_URL: user_input.get(
                        CONF_WEBHOOK_URL, DEFAULT_WEBHOOK_URL
                    ),
                }
                data = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                }
                return self.async_create_entry(
                    title=org_name, data=data, options=options
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MERAKI_API_KEY): str,
                    vol.Required(CONF_MERAKI_ORG_ID): str,
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): int,
                    vol.Optional(CONF_WEBHOOK_URL): str,
                    vol.Optional(
                        CONF_DEVICE_NAME_FORMAT, default=DEFAULT_DEVICE_NAME_FORMAT
                    ): vol.In(DEVICE_NAME_FORMAT_OPTIONS),
                    vol.Optional(CONF_AUTO_ENABLE_RTSP, default=False): bool,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)
