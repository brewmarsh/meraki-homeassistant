"""Config flow for Meraki for Home Assistant integration."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from .const.config import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_PORT_SENSORS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from .const.integration import DOMAIN

_LOGGER = logging.getLogger(__name__)

class MerakiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meraki."""
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        from .core.api import create_api_client
        from .schemas import STEP_USER_DATA_SCHEMA

        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                # Validation logic using the updated Client name
                client = create_api_client(
                    self.hass,
                    user_input[CONF_MERAKI_API_KEY],
                    user_input.get(CONF_MERAKI_ORG_ID),
                )
                await client.async_setup()
                await client.get_organizations()
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Meraki", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> MerakiOptionsFlowHandler:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)

class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Meraki options."""
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_ENABLE_DEVICE_STATUS,
                        default=self.config_entry.options.get(
                            CONF_ENABLE_DEVICE_STATUS, True
                        ),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        CONF_ENABLE_DEVICE_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_ENABLE_DEVICE_SENSORS, True
                        ),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        CONF_ENABLE_PORT_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_ENABLE_PORT_SENSORS, False
                        ),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        CONF_ENABLE_CAMERA_ENTITIES,
                        default=self.config_entry.options.get(
                            CONF_ENABLE_CAMERA_ENTITIES, True
                        ),
                    ): selector.BooleanSelector(),
                }
            ),
        )
