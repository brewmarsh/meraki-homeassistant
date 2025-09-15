"""Options flow for the Meraki Home Assistant integration."""

from typing import Any, Dict, Optional

from homeassistant import config_entries
import voluptuous as vol

from .const import CONF_INTEGRATION_TITLE
from .schemas import MENU_SCHEMA, GENERAL_SCHEMA, ADVANCED_SCHEMA


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the options flow."""
        if user_input is not None:
            # User has selected a menu item, show the corresponding form
            if user_input["next_step"] == "general":
                return await self.async_step_general()
            elif user_input["next_step"] == "advanced":
                return await self.async_step_advanced()

        # Show the menu
        return self.async_show_form(step_id="init", data_schema=MENU_SCHEMA)

    async def async_step_general(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the general settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(title=CONF_INTEGRATION_TITLE, data=self.options)

        # Populate the form with existing values
        general_schema_with_defaults = self.add_defaults_to_schema(
            GENERAL_SCHEMA, self.options
        )
        return self.async_show_form(
            step_id="general", data_schema=general_schema_with_defaults
        )

    async def async_step_advanced(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the advanced settings step."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(title=CONF_INTEGRATION_TITLE, data=self.options)

        # Populate the form with existing values
        advanced_schema_with_defaults = self.add_defaults_to_schema(
            ADVANCED_SCHEMA, self.options
        )
        return self.async_show_form(
            step_id="advanced", data_schema=advanced_schema_with_defaults
        )

    def add_defaults_to_schema(self, schema: vol.Schema, defaults: dict) -> vol.Schema:
        """Add default values to a schema."""
        new_schema = {}
        for key, value in schema.schema.items():
            if key.schema in defaults:
                # Create a new key with the default value
                new_key = vol.Required(key.schema, default=defaults[key.schema])
                new_schema[new_key] = value
            else:
                new_schema[key] = value
        return vol.Schema(new_schema)
