"""Config flow for the meraki_ha integration."""
import logging
import traceback
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID, DOMAIN
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
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        _LOGGER.debug("Meraki HA: async_step_user in config_flow.py called")
        errors: dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"User input: {user_input}")
            try:
                await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY], user_input[CONF_MERAKI_ORG_ID]
                )
                return self.async_create_entry(title="Meraki API", data=user_input)
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

    def async_config_entry_title(self, options: dict[str, Any]) -> str:
        """Return config entry title."""
        return "Meraki API"