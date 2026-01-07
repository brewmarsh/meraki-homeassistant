"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector

from .const import CONF_ENABLED_NETWORKS, CONF_INTEGRATION_TITLE, DOMAIN
from .schemas import (
    OPTIONS_SCHEMA_BASIC,
    OPTIONS_SCHEMA_CAMERA,
    OPTIONS_SCHEMA_DASHBOARD,
)


class MerakiOptionsFlowHandler(OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
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
    ) -> ConfigFlowResult:
        """
        Step 1: Basic Settings.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_dashboard()

        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                {"label": network["name"], "value": network["id"]}
                for network in coordinator.data["networks"]
            ]

        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA_BASIC,
            self.options,
            network_options,
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema_with_defaults,
        )

    async def async_step_dashboard(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Step 2: Dashboard Settings.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_camera()

        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA_DASHBOARD,
            self.options,
            [],
        )

        return self.async_show_form(
            step_id="dashboard",
            data_schema=schema_with_defaults,
        )

    async def async_step_camera(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Step 3: Camera Settings.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA_CAMERA,
            self.options,
            [],
        )

        return self.async_show_form(
            step_id="camera",
            data_schema=schema_with_defaults,
        )

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
            if key_name in defaults:
                key = type(key)(key.schema, default=defaults[key.schema])

            if key_name == CONF_ENABLED_NETWORKS and isinstance(
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = network_options
                value = selector.SelectSelector(new_config)

            new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
