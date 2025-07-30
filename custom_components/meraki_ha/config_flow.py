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

from .core.api.client import MerakiAPIClient
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_WEBHOOK_URL,
    DEFAULT_WEBHOOK_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha config_flow.py loaded")


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
                api_client = MerakiAPIClient(
                    api_key=user_input[CONF_MERAKI_API_KEY],
                    org_id=user_input[CONF_MERAKI_ORG_ID],
                )
                await api_client.get_organization()
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
                return self.async_create_entry(
                    title=user_input[CONF_MERAKI_ORG_ID], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MERAKI_API_KEY): str,
                    vol.Required(CONF_MERAKI_ORG_ID): str,
                    vol.Optional(CONF_WEBHOOK_URL): str,
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
        return MerakiOptionsFlow(config_entry)


class MerakiOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Meraki."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get("scan_interval", 60),
                    ): int,
                }
            ),
        )

    def _show_config_form(self, errors=None, user_input=None):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MERAKI_API_KEY): str,
                    vol.Required(CONF_MERAKI_ORG_ID): str,
                    vol.Optional(CONF_WEBHOOK_URL, default=DEFAULT_WEBHOOK_URL): str,
                }
            ),
            errors=errors or {},
        )
