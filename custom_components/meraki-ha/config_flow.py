"""Config flow for the meraki_ha integration."""
import logging
import traceback
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_ENTITY_ID, CONF_SCAN_INTERVAL
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID, DOMAIN, DEFAULT_SCAN_INTERVAL
from .meraki_api import validate_meraki_credentials, MerakiApiError

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)

CONFIG_FLOW = {"user": SchemaFlowFormStep(CONFIG_SCHEMA)}

class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for meraki_ha."""

    config_flow = CONFIG_FLOW

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the initial step of the config flow.

        Args:
            user_input: User input from the form.

        Returns:
            A dictionary with the next step of the flow.
        """
        _LOGGER.debug("Meraki HA: async_step_user in config_flow.py called")
        errors: Dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"User input: {user_input}")
            try:
                await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY], user_input[CONF_MERAKI_ORG_ID]
                )
                return self.async_create_entry(title="Meraki API", data=user_input)
            except ConfigEntryAuthFailed:
                errors["base"] = "invalid_auth"
            except Exception as e:
                _LOGGER.error(f"Config flow error: {e}")
                _LOGGER.error(traceback.format_exc())
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    def async_config_entry_title(self, options: Dict[str, Any]) -> str:
        """Return config entry title.

        Args:
            options: Configuration options.

        Returns:
            The config entry title.
        """
        return "Meraki API"

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Meraki integration."""

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Manage the options flow initialization.

        Args:
            user_input: User input from the form.

        Returns:
            A dictionary with the next step of the flow.
        """
        if user_input is not None:
            return self.async_create_entry(title="Meraki Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
                }
            ),
        )