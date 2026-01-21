"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

<<<<<<< HEAD
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector

from .const import CONF_ENABLED_NETWORKS, CONF_INTEGRATION_TITLE, DOMAIN
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
=======
from homeassistant import config_entries, data_entry_flow

from .const import CONF_INTEGRATION_TITLE, DOMAIN
from .coordinator import MerakiDataUpdateCoordinator
from .helpers.schema import populate_schema_defaults
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        """
        Initialize options flow.

        Args:
        ----
            config_entry: The config entry.

        """
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
<<<<<<< HEAD
    ) -> ConfigFlowResult:
=======
    ) -> data_entry_flow.FlowResult:
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        """
        Manage the options flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
<<<<<<< HEAD
        from .meraki_data_coordinator import MerakiDataCoordinator

=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

<<<<<<< HEAD
        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
=======
        coordinator: MerakiDataUpdateCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                {"label": network["name"], "value": network["id"]}
                for network in coordinator.data["networks"]
            ]

        # Populate the form with existing values from the config entry.
<<<<<<< HEAD
        schema_with_defaults = self._populate_schema_defaults(
=======
        schema_with_defaults = populate_schema_defaults(
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            OPTIONS_SCHEMA,
            self.options,
            network_options,
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)
<<<<<<< HEAD

    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
        network_options: list[dict[str, str]],
    ) -> vol.Schema:
        """
        Populate a schema with default values.

        This is used to ensure that the options form is pre-filled with the
        existing values from the config entry.

        Args:
        ----
            schema: The schema to populate.
            defaults: The default values.
            network_options: The network options.

        Returns
        -------
            The populated schema.

        """
        new_schema_keys = {}
        for key, value in schema.schema.items():
            key_name = key.schema
            # 'key.schema' is the name of the option (e.g., 'scan_interval')
            if key_name in defaults:
                # Create a new voluptuous key (e.g., vol.Required) with the
                # default value set to the existing option value.
                key = type(key)(key.schema, default=defaults[key.schema])

            if key_name == CONF_ENABLED_NETWORKS and isinstance(
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = network_options
                value = selector.SelectSelector(new_config)

            new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
