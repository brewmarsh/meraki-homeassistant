"""Config flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import callback
import voluptuous as vol

from .authentication import validate_meraki_credentials
from .const import (
    DOMAIN,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_INTEGRATION_TITLE,
)
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .options_flow import MerakiOptionsFlowHandler
from .schemas import CONFIG_SCHEMA, GENERAL_SCHEMA, ADVANCED_SCHEMA

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlowHandler(config_entries.ConfigFlow):
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
                    self.hass,
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

                # Show the general form by default
                return await self.async_step_init()

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
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the general settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.data, options=self.options
            )

        # Combine general and advanced schemas for a single configuration step
        combined_schema = vol.Schema({**GENERAL_SCHEMA.schema, **ADVANCED_SCHEMA.schema})

        return self.async_show_form(
            step_id="init",
            data_schema=combined_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)
