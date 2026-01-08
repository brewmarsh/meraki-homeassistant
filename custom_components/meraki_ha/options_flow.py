"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLE_MQTT,
    CONF_ENABLED_NETWORKS,
    CONF_INTEGRATION_TITLE,
    CONF_MQTT_RELAY_DESTINATIONS,
    DEFAULT_MQTT_PORT,
    DEFAULT_MQTT_RELAY_DESTINATIONS,
    DOMAIN,
    MQTT_DEST_HOST,
    MQTT_DEST_NAME,
    MQTT_DEST_PASSWORD,
    MQTT_DEST_PORT,
    MQTT_DEST_TOPIC_FILTER,
    MQTT_DEST_USE_TLS,
    MQTT_DEST_USERNAME,
)
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
        self._editing_destination_index: int | None = None

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
        """
        Step 4: MQTT Settings.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        if user_input is not None:
            # Handle MQTT enable/disable separately from relay management
            self.options[CONF_ENABLE_MQTT] = user_input.get(CONF_ENABLE_MQTT, False)

            # Check if there's an action to add a destination
            if user_input.get("add_relay_destination"):
                self._editing_destination_index = None
                return await self.async_step_mqtt_destination()

            # Check if user wants to manage existing destinations
            if user_input.get("manage_relay_destinations"):
                return await self.async_step_mqtt_manage_relays()

            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

        # Build the schema with current relay destinations info
        current_destinations = self.options.get(
            CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
        )
        destinations_summary = ""
        if current_destinations:
            destinations_summary = ", ".join(
                d.get(MQTT_DEST_NAME, d.get(MQTT_DEST_HOST, "Unknown"))
                for d in current_destinations
            )

        # Build schema dynamically based on whether destinations exist
        mqtt_schema = {
            vol.Required(
                CONF_ENABLE_MQTT,
                default=self.options.get(CONF_ENABLE_MQTT, False),
            ): selector.BooleanSelector(),
            vol.Optional(
                "add_relay_destination", default=False
            ): selector.BooleanSelector(),
        }

        # Add manage button if there are destinations to manage
        if current_destinations:
            mqtt_schema[vol.Optional("manage_relay_destinations", default=False)] = (
                selector.BooleanSelector()
            )

        return self.async_show_form(
            step_id="mqtt",
            data_schema=vol.Schema(mqtt_schema),
            description_placeholders={
                "relay_destinations": destinations_summary or "None configured",
                "destination_count": str(len(current_destinations)),
            },
        )

    async def async_step_mqtt_manage_relays(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Sub-step: Manage existing MQTT Relay Destinations.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        current_destinations = self.options.get(
            CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
        )

        if user_input is not None:
            action = user_input.get("action", "back")
            selected_dest = user_input.get("destination_index")

            # Find the index by matching the display string
            idx = None
            if selected_dest:
                for i, d in enumerate(current_destinations):
                    display = (
                        f"{d.get(MQTT_DEST_NAME, 'Unnamed')} ({d.get(MQTT_DEST_HOST)})"
                    )
                    if display == selected_dest:
                        idx = i
                        break

            if action == "edit" and idx is not None:
                self._editing_destination_index = idx
                return await self.async_step_mqtt_destination()
            if action == "delete" and idx is not None:
                if 0 <= idx < len(current_destinations):
                    current_destinations = list(current_destinations)
                    del current_destinations[idx]
                    self.options[CONF_MQTT_RELAY_DESTINATIONS] = current_destinations
                return await self.async_step_mqtt()
            return await self.async_step_mqtt()

        # Build list of destinations for selection
        destination_options: list[str] = [
            f"{d.get(MQTT_DEST_NAME, 'Unnamed')} ({d.get(MQTT_DEST_HOST)})"
            for d in current_destinations
        ]

        manage_schema = vol.Schema(
            {
                vol.Required("destination_index"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=destination_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required("action", default="edit"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=["edit", "delete", "back"],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="mqtt_relay_action",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="mqtt_manage_relays",
            data_schema=manage_schema,
        )

    async def async_step_mqtt_destination(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Sub-step: Add/Edit MQTT Relay Destination.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        errors: dict[str, str] = {}
        is_editing = self._editing_destination_index is not None

        if user_input is not None:
            # Validate the destination configuration
            if not user_input.get(MQTT_DEST_HOST):
                errors["base"] = "host_required"
            elif not user_input.get(MQTT_DEST_NAME):
                errors["base"] = "name_required"
            else:
                current_destinations = list(
                    self.options.get(
                        CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
                    )
                )

                if is_editing and self._editing_destination_index is not None:
                    # Update existing destination
                    idx = self._editing_destination_index
                    if 0 <= idx < len(current_destinations):
                        current_destinations[idx] = user_input
                else:
                    # Add new destination
                    current_destinations.append(user_input)

                self.options[CONF_MQTT_RELAY_DESTINATIONS] = current_destinations
                self._editing_destination_index = None

                # Return to MQTT step to show updated list or finish
                return await self.async_step_mqtt()

        # Build schema with defaults for editing
        defaults = {}
        if is_editing and self._editing_destination_index is not None:
            current_destinations = self.options.get(
                CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
            )
            if 0 <= self._editing_destination_index < len(current_destinations):
                defaults = current_destinations[self._editing_destination_index]

        destination_schema = vol.Schema(
            {
                vol.Required(
                    MQTT_DEST_NAME,
                    default=defaults.get(MQTT_DEST_NAME, ""),
                ): selector.TextSelector(),
                vol.Required(
                    MQTT_DEST_HOST,
                    default=defaults.get(MQTT_DEST_HOST, ""),
                ): selector.TextSelector(),
                vol.Optional(
                    MQTT_DEST_PORT,
                    default=defaults.get(MQTT_DEST_PORT, DEFAULT_MQTT_PORT),
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=65535, mode=selector.NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(
                    MQTT_DEST_USERNAME,
                    default=defaults.get(MQTT_DEST_USERNAME, ""),
                ): selector.TextSelector(),
                vol.Optional(
                    MQTT_DEST_PASSWORD,
                    default=defaults.get(MQTT_DEST_PASSWORD, ""),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
                ),
                vol.Optional(
                    MQTT_DEST_USE_TLS,
                    default=defaults.get(MQTT_DEST_USE_TLS, False),
                ): selector.BooleanSelector(),
                vol.Optional(
                    MQTT_DEST_TOPIC_FILTER,
                    default=defaults.get(MQTT_DEST_TOPIC_FILTER, "meraki/v1/mt/#"),
                ): selector.TextSelector(),
            }
        )

        return self.async_show_form(
            step_id="mqtt_destination",
            data_schema=destination_schema,
            errors=errors,
            description_placeholders={
                "action": "Edit" if is_editing else "Add",
            },
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
