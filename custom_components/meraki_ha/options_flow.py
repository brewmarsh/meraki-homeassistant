"""Options flow for the Meraki Home Assistant integration."""

from typing import Any, Dict, Optional

from homeassistant import config_entries
import voluptuous as vol

from .const import CONF_INTEGRATION_TITLE
from .schemas import GENERAL_SCHEMA, ADVANCED_SCHEMA, FEATURES_SCHEMA


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
            self.options.update(user_input)
            return self.async_create_entry(title=CONF_INTEGRATION_TITLE, data=self.options)

        # Combine all schemas into a single view
        combined_schema = vol.Schema(
            {
                **GENERAL_SCHEMA.schema,
                **ADVANCED_SCHEMA.schema,
                **FEATURES_SCHEMA.schema,
            }
        )

        # Populate the form with existing values
        schema_with_defaults = self.add_defaults_to_schema(
            combined_schema, self.options
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)

    def add_defaults_to_schema(self, schema: vol.Schema, defaults: dict) -> vol.Schema:
        """Add default values to a schema."""
        new_schema = {}
        for key, value in schema.schema.items():
            if key.schema in defaults:
                # Create a new key with the default value, preserving whether it's optional
                new_key = type(key)(key.schema, default=defaults[key.schema])
                new_schema[new_key] = value
            else:
                new_schema[key] = value
        return vol.Schema(new_schema)