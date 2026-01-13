"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
<<<<<<< HEAD
<<<<<<< HEAD
from homeassistant import config_entries, data_entry_flow
=======
<<<<<<< HEAD
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector

from .const import CONF_IGNORED_NETWORKS, CONF_INTEGRATION_TITLE, DOMAIN
from .coordinator import MerakiDataUpdateCoordinator
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
from homeassistant.helpers import selector

from .const import CONF_IGNORED_NETWORKS, CONF_INTEGRATION_TITLE, DOMAIN
from .coordinator import MerakiDataUpdateCoordinator
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

<<<<<<< HEAD
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
=======
    def __init__(self, config_entry: ConfigEntry) -> None:
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
    ) -> data_entry_flow.FlowResult:
=======
<<<<<<< HEAD
    ) -> data_entry_flow.FlowResult:
=======
    ) -> ConfigFlowResult:
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    ) -> ConfigFlowResult:
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
        from .meraki_data_coordinator import MerakiDataCoordinator

>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        from .meraki_data_coordinator import MerakiDataCoordinator

>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]
=======
        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                {"label": network["name"], "value": network["id"]}
                for network in coordinator.data["networks"]
            ]

        # Populate the form with existing values from the config entry.
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA,
            self.options,
            network_options,
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
        network_options: list[dict[str, str]],
    ) -> vol.Schema:
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    @staticmethod
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
        network_options: list[dict[str, str]],
<<<<<<< HEAD
    ) -> vol.Schema:
=======
    ):
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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

<<<<<<< HEAD
<<<<<<< HEAD
            if key_name == CONF_IGNORED_NETWORKS and isinstance(
=======
<<<<<<< HEAD
            if key_name == CONF_IGNORED_NETWORKS and isinstance(
=======
            if key_name == CONF_ENABLED_NETWORKS and isinstance(
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
            if key_name == CONF_ENABLED_NETWORKS and isinstance(
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = network_options
                value = selector.SelectSelector(new_config)

            new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
