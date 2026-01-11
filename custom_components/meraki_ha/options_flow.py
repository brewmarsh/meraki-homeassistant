"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlowResult, OptionsFlow
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
    SCHEMA_CAMERA,
    SCHEMA_DISPLAY_PREFERENCES,
    SCHEMA_LOGGING,
    SCHEMA_NETWORK_SELECTION,
    SCHEMA_POLLING,
)


class MerakiOptionsFlowHandler(OptionsFlow):
    """Handle an options flow for the Meraki integration.

    Note: As of Home Assistant 2025.x, the OptionsFlow class no longer accepts
    config_entry as a constructor parameter. The config_entry is set by the
    framework after initialization and is available through self.config_entry
    property in async steps (but NOT in __init__).
    """

    def __init__(self) -> None:
        """Initialize options flow."""
        super().__init__()
        self._options: dict[str, Any] = {}
        self._destination_action: str | None = None
        self._editing_destination_index: int | None = None
        self._options_initialized: bool = False

    @property
    def options(self) -> dict[str, Any]:
        """Return the current options.

        Lazily initializes from config_entry.options on first access
        in an async step context.
        """
        if not self._options_initialized and hasattr(self, "hass") and self.hass:
            try:
                self._options = dict(self.config_entry.options)
                self._options_initialized = True
            except ValueError:
                # config_entry not available yet (during initialization)
                pass
        return self._options

    @options.setter
    def options(self, value: dict[str, Any]) -> None:
        """Set the options dict."""
        self._options = value
        self._options_initialized = True

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Show the main menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=[
                "network_selection",
                "polling",
                "camera",
                "mqtt",
                "scanning_api",
                "display_preferences",
                "notifications",
                "logging",
            ],
        )

    async def async_step_scanning_api(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle Scanning API settings."""
        from .const import (
            CONF_SCANNING_API_EXTERNAL_URL,
            CONF_SCANNING_API_VALIDATOR,
            DEFAULT_SCANNING_API_EXTERNAL_URL,
            DEFAULT_SCANNING_API_VALIDATOR,
        )
        from .core.errors import MerakiConnectionError
        from .schemas import SCHEMA_SCANNING_API
        from .webhook import get_webhook_url

        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        # Get current options for URL generation
        custom_url = self.options.get(
            CONF_SCANNING_API_EXTERNAL_URL, DEFAULT_SCANNING_API_EXTERNAL_URL
        )
        validator = self.options.get(
            CONF_SCANNING_API_VALIDATOR, DEFAULT_SCANNING_API_VALIDATOR
        )

        # Generate the full webhook URL to display to the user
        try:
            # Use custom URL if provided, otherwise use HA's external URL
            base_webhook_url = get_webhook_url(
                self.hass, self.config_entry.entry_id, custom_url or None
            )
            # Append validator to the URL if configured
            if validator:
                webhook_url = f"{base_webhook_url}/{validator}"
            else:
                webhook_url = f"{base_webhook_url}/YOUR_VALIDATOR_HERE"
        except MerakiConnectionError as err:
            webhook_url = f"⚠️ {err}"

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_SCANNING_API,
            self.options,
        )

        return self.async_show_form(
            step_id="scanning_api",
            data_schema=schema_with_defaults,
            description_placeholders={"webhook_url": webhook_url},
        )

    async def async_step_network_selection(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle network selection settings."""
        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
        network_options: list[selector.SelectOptionDict] = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                selector.SelectOptionDict(label=network["name"], value=network["id"])
                for network in coordinator.data["networks"]
            ]

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_NETWORK_SELECTION,
            self.options,
            network_options,
        )

        return self.async_show_form(
            step_id="network_selection",
            data_schema=schema_with_defaults,
        )

    async def async_step_polling(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle polling settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_POLLING,
            self.options,
        )

        return self.async_show_form(
            step_id="polling",
            data_schema=schema_with_defaults,
        )

    async def async_step_camera(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle camera settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_CAMERA,
            self.options,
        )

        return self.async_show_form(
            step_id="camera",
            data_schema=schema_with_defaults,
        )

    async def async_step_display_preferences(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle display preferences."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_DISPLAY_PREFERENCES,
            self.options,
        )

        return self.async_show_form(
            step_id="display_preferences",
            data_schema=schema_with_defaults,
        )

    async def async_step_notifications(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle notifications settings (coming soon placeholder)."""
        if user_input is not None:
            # Return to menu when user clicks submit
            return await self.async_step_init()

        return self.async_show_form(
            step_id="notifications",
            data_schema=vol.Schema({}),
            description_placeholders={
                "message": "Notification settings will be available in a future update."
            },
        )

    async def async_step_logging(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle logging settings."""
        from .helpers.logging_helper import apply_log_levels

        if user_input is not None:
            self.options.update(user_input)
            # Apply the log levels immediately
            apply_log_levels(self.options)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_LOGGING,
            self.options,
        )

        return self.async_show_form(
            step_id="logging",
            data_schema=schema_with_defaults,
        )

    async def async_step_mqtt(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """MQTT Settings Menu."""
        if user_input is not None:
            self.options[CONF_ENABLE_MQTT] = user_input[CONF_ENABLE_MQTT]
            action = user_input.get("action", "save")

            if action == "add":
                self._editing_destination_index = None
                return await self.async_step_mqtt_destination()
            if action == "edit":
                self._destination_action = "edit"
                return await self.async_step_mqtt_select_destination()
            if action == "delete":
                self._destination_action = "delete"
                return await self.async_step_mqtt_select_destination()

            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        current_destinations = self.options.get(
            CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
        )

        actions = [
            selector.SelectOptionDict(value="save", label="Save and Finish"),
            selector.SelectOptionDict(value="add", label="Add new relay destination"),
        ]
        if current_destinations:
            actions.append(
                selector.SelectOptionDict(
                    value="edit", label="Edit existing destination"
                )
            )
            actions.append(
                selector.SelectOptionDict(value="delete", label="Delete a destination")
            )

        schema_with_defaults = vol.Schema(
            {
                vol.Required(
                    CONF_ENABLE_MQTT,
                    default=self.options.get(CONF_ENABLE_MQTT, False),
                ): selector.BooleanSelector(),
                vol.Optional("action", default="save"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=actions,
                        mode=selector.SelectSelectorMode.LIST,
                        translation_key="mqtt_relay_menu_action",
                    )
                ),
            }
        )
        destinations_summary = ", ".join(
            d.get(MQTT_DEST_NAME, d.get(MQTT_DEST_HOST, "Unknown"))
            for d in current_destinations
        )

        return self.async_show_form(
            step_id="mqtt",
            data_schema=schema_with_defaults,
            description_placeholders={
                "destination_count": str(len(current_destinations)),
                "relay_destinations": destinations_summary or "None",
            },
        )

    async def async_step_mqtt_select_destination(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select a destination to edit or delete."""
        action = self._destination_action or "edit"
        current_destinations = self.options.get(
            CONF_MQTT_RELAY_DESTINATIONS, DEFAULT_MQTT_RELAY_DESTINATIONS
        )

        if not current_destinations:
            self._destination_action = None
            return await self.async_step_mqtt()

        destination_options: list[selector.SelectOptionDict] = [
            selector.SelectOptionDict(
                value=str(i),
                label=f"{d.get(MQTT_DEST_NAME, 'Unnamed')} ({d.get(MQTT_DEST_HOST)})",
            )
            for i, d in enumerate(current_destinations)
        ]

        if user_input is not None:
            selected_indices = [int(i) for i in user_input.get("destinations", [])]

            if action == "edit":
                if selected_indices:
                    self._editing_destination_index = selected_indices[0]
                    self._destination_action = None
                    return await self.async_step_mqtt_destination()
                self._destination_action = None
                return await self.async_step_mqtt()

            if action == "delete":
                destinations = list(current_destinations)
                for idx in sorted(selected_indices, reverse=True):
                    if 0 <= idx < len(destinations):
                        del destinations[idx]
                self.options[CONF_MQTT_RELAY_DESTINATIONS] = destinations
                self._destination_action = None
                return await self.async_step_mqtt()

        schema = vol.Schema(
            {
                vol.Required("destinations"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=destination_options,
                        multiple=(action == "delete"),
                        mode=selector.SelectSelectorMode.LIST,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="mqtt_select_destination",
            data_schema=schema,
            description_placeholders={"action": action.capitalize()},
        )

    async def async_step_mqtt_destination(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Add/Edit MQTT Relay Destination."""
        errors: dict[str, str] = {}
        is_editing = self._editing_destination_index is not None

        if user_input is not None:
            if not user_input.get(MQTT_DEST_HOST):
                errors["base"] = "host_required"
            elif not user_input.get(MQTT_DEST_NAME):
                errors["base"] = "name_required"
            else:
                destinations = list(self.options.get(CONF_MQTT_RELAY_DESTINATIONS, []))
                if MQTT_DEST_PORT in user_input:
                    try:
                        user_input[MQTT_DEST_PORT] = int(user_input[MQTT_DEST_PORT])
                    except (ValueError, TypeError):
                        errors["base"] = "invalid_port"

                if not errors:
                    if is_editing and self._editing_destination_index is not None:
                        idx = self._editing_destination_index
                        if 0 <= idx < len(destinations):
                            destinations[idx] = user_input
                    else:
                        destinations.append(user_input)

                    self.options[CONF_MQTT_RELAY_DESTINATIONS] = destinations
                    self._editing_destination_index = None
                    return await self.async_step_mqtt()

        defaults = {}
        if is_editing and self._editing_destination_index is not None:
            destinations = self.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])
            if 0 <= self._editing_destination_index < len(destinations):
                defaults = destinations[self._editing_destination_index]

        destination_schema = vol.Schema(
            {
                vol.Required(
                    MQTT_DEST_NAME, default=defaults.get(MQTT_DEST_NAME, "")
                ): selector.TextSelector(),
                vol.Required(
                    MQTT_DEST_HOST, default=defaults.get(MQTT_DEST_HOST, "")
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
                    MQTT_DEST_USERNAME, default=defaults.get(MQTT_DEST_USERNAME, "")
                ): selector.TextSelector(),
                vol.Optional(
                    MQTT_DEST_PASSWORD, default=defaults.get(MQTT_DEST_PASSWORD, "")
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
                ),
                vol.Optional(
                    MQTT_DEST_USE_TLS, default=defaults.get(MQTT_DEST_USE_TLS, False)
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
            description_placeholders={"action": "Edit" if is_editing else "Add"},
        )

    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
        network_options: list[selector.SelectOptionDict] | None = None,
    ) -> vol.Schema:
        """Populate a schema with default values."""
        new_schema_keys = {}
        for key, value in schema.schema.items():
            key_name = key.schema
            if key_name in defaults:
                key = type(key)(key_name, default=defaults[key_name])

            if (
                key_name == CONF_ENABLED_NETWORKS
                and network_options is not None
                and isinstance(value, selector.SelectSelector)
            ):
                value.config["options"] = network_options

            new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
