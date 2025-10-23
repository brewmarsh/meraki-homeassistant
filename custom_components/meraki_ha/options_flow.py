"""Options flow for the Meraki Home Assistant integration."""

from typing import Any, Dict, Optional

from homeassistant import config_entries
import voluptuous as vol

from .const import CONF_INTEGRATION_TITLE
from .schemas import OPTIONS_SCHEMA


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
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        # Populate the form with existing values from the config entry.
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA, self.options
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)

    def _populate_schema_defaults(
        self, schema: vol.Schema, defaults: dict
    ) -> vol.Schema:
        """
        Populate a schema with default values.

        This is used to ensure that the options form is pre-filled with the
        existing values from the config entry.
        """
        new_schema_keys = {}
        for key, value in schema.schema.items():
            # 'key.schema' is the name of the option (e.g., 'scan_interval')
            if key.schema in defaults:
                # Create a new voluptuous key (e.g., vol.Required) with the
                # default value set to the existing option value.
                new_key = type(key)(key.schema, default=defaults[key.schema])
                new_schema_keys[new_key] = value
            else:
                new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
