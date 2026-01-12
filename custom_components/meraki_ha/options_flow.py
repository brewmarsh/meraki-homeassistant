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
    CONF_MANUAL_CLIENT_ASSOCIATIONS,
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
    SCHEMA_DATA_SYNC,
    SCHEMA_DISPLAY_PREFERENCES,
    SCHEMA_LOGGING,
    SCHEMA_NETWORK_SELECTION,
    SCHEMA_POLLING,
    SCHEMA_WEBHOOKS,
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
                "device_association",
                "polling",
                "webhooks",
                "data_sync",
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

    async def async_step_device_association(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle device association settings - main menu."""
        from homeassistant.helpers import device_registry as dr

        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            action = user_input.get("action", "save")

            if action == "add":
                return await self.async_step_select_client()
            if action == "remove":
                return await self.async_step_remove_association()

            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        # Get current associations
        current_associations: dict[str, str] = self.options.get(
            CONF_MANUAL_CLIENT_ASSOCIATIONS, {}
        )

        # Build summary of current associations
        association_summary = []
        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
        device_registry = dr.async_get(self.hass)

        for client_mac, device_id in current_associations.items():
            # Find client name
            client_name = client_mac
            if coordinator.data and coordinator.data.get("clients"):
                for client in coordinator.data["clients"]:
                    if client.get("mac") == client_mac:
                        client_name = (
                            client.get("description")
                            or client.get("dhcpHostname")
                            or client_mac
                        )
                        break

            # Find device name
            device = device_registry.async_get(device_id)
            device_name = device.name if device else device_id

            association_summary.append(f"• {client_name} → {device_name}")

        summary_text = "\n".join(association_summary) if association_summary else "None"

        actions = [
            selector.SelectOptionDict(value="save", label="✓ Save and return to menu"),
            selector.SelectOptionDict(
                value="add", label="+ Add new client → device association"
            ),
        ]
        if current_associations:
            actions.append(
                selector.SelectOptionDict(
                    value="remove", label="− Remove an existing association"
                )
            )

        schema = vol.Schema(
            {
                vol.Optional("action", default="save"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=actions,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="device_association",
            data_schema=schema,
            description_placeholders={
                "association_count": str(len(current_associations)),
                "associations": summary_text,
            },
        )

    async def async_step_select_client(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select a Meraki client to associate with an HA device."""
        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            # Store selected client MAC and proceed to device selection
            self._selected_client_mac = user_input.get("client")
            return await self.async_step_select_device()

        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]

        # Get current associations to filter out already-associated clients
        current_associations: dict[str, str] = self.options.get(
            CONF_MANUAL_CLIENT_ASSOCIATIONS, {}
        )

        # Build list of unassociated clients
        client_options: list[selector.SelectOptionDict] = []
        if coordinator.data and coordinator.data.get("clients"):
            for client in coordinator.data["clients"]:
                client_mac = client.get("mac")
                if not client_mac or client_mac in current_associations:
                    continue

                # Generate friendly name
                client_name = (
                    client.get("description")
                    or client.get("dhcpHostname")
                    or client.get("ip")
                    or client_mac
                )
                manufacturer = client.get("manufacturer", "")
                if manufacturer:
                    label = f"{client_name} ({manufacturer})"
                else:
                    label = client_name

                client_options.append(
                    selector.SelectOptionDict(value=client_mac, label=label)
                )

        if not client_options:
            # No clients available
            return self.async_show_form(
                step_id="select_client",
                data_schema=vol.Schema({}),
                description_placeholders={
                    "message": "No unassociated clients available."
                },
                errors={"base": "no_clients"},
            )

        # Sort by label
        client_options.sort(key=lambda x: x["label"].lower())

        schema = vol.Schema(
            {
                vol.Required("client"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=client_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="select_client",
            data_schema=schema,
        )

    async def async_step_select_device(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select an HA device to link the Meraki client to."""
        from homeassistant.helpers import device_registry as dr

        if user_input is not None:
            # Save the association
            device_id = user_input.get("device")
            client_mac = getattr(self, "_selected_client_mac", None)

            if client_mac and device_id:
                associations = dict(
                    self.options.get(CONF_MANUAL_CLIENT_ASSOCIATIONS, {})
                )
                associations[client_mac] = device_id
                self.options[CONF_MANUAL_CLIENT_ASSOCIATIONS] = associations

            # Clean up and return to main menu
            self._selected_client_mac = None
            return await self.async_step_device_association()

        # Build list of HA devices (excluding Meraki client devices)
        device_registry = dr.async_get(self.hass)
        device_options: list[selector.SelectOptionDict] = []

        for device in device_registry.devices.values():
            # Skip Meraki client devices
            if any(
                DOMAIN in str(ident) and "client_" in str(ident)
                for ident in device.identifiers
            ):
                continue

            # Skip devices without a name
            if not device.name:
                continue

            # Include manufacturer info if available
            if device.manufacturer:
                label = f"{device.name} ({device.manufacturer})"
            else:
                label = device.name

            device_options.append(
                selector.SelectOptionDict(value=device.id, label=label)
            )

        if not device_options:
            return self.async_show_form(
                step_id="select_device",
                data_schema=vol.Schema({}),
                errors={"base": "no_devices"},
            )

        # Sort by label
        device_options.sort(key=lambda x: x["label"].lower())

        schema = vol.Schema(
            {
                vol.Required("device"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=device_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="select_device",
            data_schema=schema,
        )

    async def async_step_remove_association(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Remove an existing device association."""
        from homeassistant.helpers import device_registry as dr

        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            # Remove selected associations
            selected_macs = user_input.get("associations", [])
            if selected_macs:
                associations = dict(
                    self.options.get(CONF_MANUAL_CLIENT_ASSOCIATIONS, {})
                )
                for mac in selected_macs:
                    associations.pop(mac, None)
                self.options[CONF_MANUAL_CLIENT_ASSOCIATIONS] = associations

            return await self.async_step_device_association()

        # Build list of current associations
        current_associations: dict[str, str] = self.options.get(
            CONF_MANUAL_CLIENT_ASSOCIATIONS, {}
        )

        if not current_associations:
            return await self.async_step_device_association()

        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]
        device_registry = dr.async_get(self.hass)

        association_options: list[selector.SelectOptionDict] = []
        for client_mac, device_id in current_associations.items():
            # Find client name
            client_name = client_mac
            if coordinator.data and coordinator.data.get("clients"):
                for client in coordinator.data["clients"]:
                    if client.get("mac") == client_mac:
                        client_name = (
                            client.get("description")
                            or client.get("dhcpHostname")
                            or client_mac
                        )
                        break

            # Find device name
            device = device_registry.async_get(device_id)
            device_name = device.name if device else device_id

            association_options.append(
                selector.SelectOptionDict(
                    value=client_mac, label=f"{client_name} → {device_name}"
                )
            )

        schema = vol.Schema(
            {
                vol.Required("associations"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=association_options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="remove_association",
            data_schema=schema,
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

    async def async_step_webhooks(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle webhook settings."""
        from .const import (
            CONF_WEBHOOK_EXTERNAL_URL,
            DEFAULT_WEBHOOK_EXTERNAL_URL,
        )
        from .core.errors import MerakiConnectionError
        from .webhook import get_webhook_url

        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        custom_url = self.options.get(
            CONF_WEBHOOK_EXTERNAL_URL, DEFAULT_WEBHOOK_EXTERNAL_URL
        )

        try:
            webhook_url = get_webhook_url(
                self.hass, self.config_entry.entry_id, custom_url or None
            )
        except MerakiConnectionError as err:
            webhook_url = f"⚠️ {err}"

        # Get real webhook status from coordinator
        status = self._get_webhook_status()

        # Provide manual setup guidance if available from WebhookManager
        manual_setup = ""
        entry_data = self.hass.data.get(DOMAIN, {}).get(self.config_entry.entry_id, {})
        webhook_manager = entry_data.get("webhook_manager")
        if webhook_manager:
            manual = webhook_manager.get_manual_setup_instructions()
            url = manual.get("webhook_url", "N/A")
            secret = manual.get("shared_secret", "N/A")
            alert_types = ", ".join(manual.get("alert_types", [])) or "None"
            manual_setup = (
                "Manual setup (use if auto-register fails):\n"
                f"URL: {url}\nSecret: {secret}\nAlerts: {alert_types}"
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_WEBHOOKS,
            self.options,
        )

        return self.async_show_form(
            step_id="webhooks",
            data_schema=schema_with_defaults,
            description_placeholders={
                "webhook_url": webhook_url,
                "status": status,
                "manual_setup": manual_setup,
            },
        )

    def _get_webhook_status(self) -> str:
        """Get the current webhook status from the coordinator."""
        from .const import DOMAIN

        try:
            entry_data = self.hass.data.get(DOMAIN, {}).get(
                self.config_entry.entry_id, {}
            )
            # Prefer WebhookManager status if available
            webhook_manager = entry_data.get("webhook_manager")
            if webhook_manager:
                status = webhook_manager.webhook_status
                base_msg = status.get("message", "❓ Unable to determine status")
                # Include manual setup hint if auto-registration failed
                if status.get("status") == "error":
                    manual = webhook_manager.get_manual_setup_instructions()
                    url = manual.get("webhook_url", "N/A")
                    secret = manual.get("shared_secret", "N/A")
                    alert_types = ", ".join(manual.get("alert_types", [])) or "None"
                    return (
                        f"{base_msg}\nManual setup:\nURL: {url}\nSecret: {secret}\n"
                        f"Alerts: {alert_types}"
                    )
                return base_msg

            coordinator = entry_data.get("coordinator")

            if not coordinator:
                return "❓ Coordinator not available"

            # Check if webhooks are active (received recently)
            if hasattr(coordinator, "webhooks_active") and coordinator.webhooks_active:
                stats = getattr(coordinator, "webhook_stats", {})
                count = stats.get("total_received", 0)
                return f"✅ Webhooks active ({count} received)"

            # Check if webhooks were ever received
            if hasattr(coordinator, "webhook_stats"):
                stats = coordinator.webhook_stats
                if stats.get("last_received"):
                    return "⚠️ Webhooks configured but not recently active"

            # Check if webhook is registered with HA
            webhook_id = self.config_entry.data.get("webhook_id")
            if webhook_id:
                return "✅ Webhook registered with Home Assistant"

            return "❌ Webhooks not configured"

        except Exception:
            return "❓ Unable to determine status"

    async def async_step_data_sync(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle data sync settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema_with_defaults = self._populate_schema_defaults(
            SCHEMA_DATA_SYNC,
            self.options,
        )

        return self.async_show_form(
            step_id="data_sync",
            data_schema=schema_with_defaults,
        )
