"""Config flow for the meraki_ha integration."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)

from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID, DOMAIN
from .meraki_api import validate_meraki_credentials
from .sensor import async_setup_entry as async_setup_sensor_entry

_LOGGER = logging.getLogger(__name__)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
            selector.EntitySelectorConfig(domain=SENSOR_DOMAIN)
        ),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)

CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA)
}

OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(OPTIONS_SCHEMA)
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for meraki_ha."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"User input: {user_input}")  # Log the user input.
            try:
                await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY], user_input[CONF_MERAKI_ORG_ID]
                )
                _LOGGER.debug(
                    f"Data to be saved: {user_input}"
                )  # Log the data to be saved.
                result = await self.async_create_entry(data=user_input)
                _LOGGER.debug(f"async_create_entry result: {result}")  # Log the result.
                return result  # Return the result of async_create_entry.
            except ConfigEntryAuthFailed:
                errors["base"] = "invalid_auth"
            except Exception as e:
                _LOGGER.error(f"Config flow error: {e}")  # Log the exception.
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return "Meraki API"


async def async_setup_entry(hass, config_entry):
    """Set up the Meraki integration."""
    return await async_setup_sensor_entry(hass, config_entry, hass.async_add_entities)


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    return True
