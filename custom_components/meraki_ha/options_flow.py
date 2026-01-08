"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLED_NETWORKS,
    CONF_MQTT_RELAY_DESTINATIONS,
    DOMAIN,
)
from .schemas import (
    MQTT_DESTINATION_SCHEMA,
    OPTIONS_SCHEMA_BASIC,
    OPTIONS_SCHEMA_CAMERA,
    OPTIONS_SCHEMA_DASHBOARD,
)


class MerakiOptionsFlowHandler(OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    _destination_index_to_edit: int | None = None

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
            return await self.async_step_mqtt()

        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA_CAMERA,
            self.options,
            [],
        )

        return self.async_show_form(
            step_id="camera",
            data_schema=schema_with_defaults,
        )

    async def async_step_mqtt(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Step 4: MQTT Settings Menu."""
        return self.async_show_menu(
            step_id="mqtt",
            menu_options=[
                "mqtt_add_destination",
                "mqtt_edit_destination",
                "mqtt_delete_destination",
            ],
        )

    async def async_step_mqtt_add_destination(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add a new MQTT destination."""
        if user_input is not None:
            destinations = self.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])
            destinations.append(user_input)
            self.options[CONF_MQTT_RELAY_DESTINATIONS] = destinations
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="mqtt_add_destination",
            data_schema=MQTT_DESTINATION_SCHEMA,
        )

    async def async_step_mqtt_edit_destination(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the start of the edit flow or the form submission."""
        destinations = self.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])

        if not destinations:
            return self.async_abort(reason="no_destinations")

        if user_input is not None:
            if "destination_index" in user_input:
                self._destination_index_to_edit = user_input["destination_index"]
                destination_to_edit = destinations[self._destination_index_to_edit]
                return self.async_show_form(
                    step_id="mqtt_edit_destination",
                    data_schema=vol.Schema(
                        {
                            vol.Required(
                                "server_ip", default=destination_to_edit["server_ip"]
                            ): selector.TextSelector(),
                            vol.Required(
                                "port", default=destination_to_edit["port"]
                            ): selector.NumberSelector(
                                selector.NumberSelectorConfig(
                                    min=1,
                                    max=65535,
                                    mode=selector.NumberSelectorMode.BOX,
                                ),
                            ),
                            vol.Required(
                                "topic", default=destination_to_edit["topic"]
                            ): selector.TextSelector(),
                        }
                    ),
                    description_placeholders={
                        "destination_label": (
                            f"{destination_to_edit['server_ip']}:"
                            f"{destination_to_edit['port']}"
                        )
                    },
                )
            else:
                if self._destination_index_to_edit is not None:
                    destinations[self._destination_index_to_edit] = user_input
                    self.options[CONF_MQTT_RELAY_DESTINATIONS] = destinations
                    self._destination_index_to_edit = None
                    return self.async_create_entry(title="", data=self.options)

        destination_options = [
            selector.SelectOptionDict(
                value=str(i), label=f"{d['server_ip']}:{d['port']}"
            )
            for i, d in enumerate(destinations)
        ]
        return self.async_show_form(
            step_id="mqtt_edit_destination",
            data_schema=vol.Schema(
                {
                    vol.Required("destination_index"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=destination_options,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
        )

    async def async_step_mqtt_delete_destination(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Delete one or more MQTT destinations."""
        destinations = self.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])

        if not destinations:
            return self.async_abort(reason="no_destinations")

        if user_input is not None:
            indices_to_delete = {
                int(i) for i in user_input.get("destinations_to_delete", [])
            }
            self.options[CONF_MQTT_RELAY_DESTINATIONS] = [
                dest
                for i, dest in enumerate(destinations)
                if i not in indices_to_delete
            ]
            return self.async_create_entry(title="", data=self.options)

        destination_options = [
            selector.SelectOptionDict(
                value=str(i), label=f"{d['server_ip']}:{d['port']}"
            )
            for i, d in enumerate(destinations)
        ]
        return self.async_show_form(
            step_id="mqtt_delete_destination",
            data_schema=vol.Schema(
                {
                    vol.Required("destinations_to_delete"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=destination_options, multiple=True
                        )
                    ),
                }
            ),
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
