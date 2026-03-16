"""Config flow for Meraki for Home Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from homeassistant import config_entries

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

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        from .core.api import create_api_client
        from .core.errors import (
            InvalidOrgID,
            MerakiAuthenticationError,
            MerakiConnectionError,
        )
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
            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
            except InvalidOrgID:
                errors["base"] = "invalid_org_id"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Cisco Meraki", data=user_input)

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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["general", "sensors", "cameras", "advanced"],
        )

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle general settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import OPTIONS_SCHEMA_GENERAL

        return self.async_show_form(
            step_id="general",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA_GENERAL, self.config_entry.options
            ),
        )

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle sensor settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import OPTIONS_SCHEMA_SENSORS

        return self.async_show_form(
            step_id="sensors",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA_SENSORS, self.config_entry.options
            ),
        )

    async def async_step_cameras(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle camera settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import OPTIONS_SCHEMA_CAMERAS

        return self.async_show_form(
            step_id="cameras",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA_CAMERAS, self.config_entry.options
            ),
        )

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle advanced settings."""
        if user_input is not None:
            return self.async_create_entry(
                title="", data=self.config_entry.options | user_input
            )

        from .schemas import OPTIONS_SCHEMA_ADVANCED

        return self.async_show_form(
            step_id="advanced",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA_ADVANCED, self.config_entry.options
            ),
        )
