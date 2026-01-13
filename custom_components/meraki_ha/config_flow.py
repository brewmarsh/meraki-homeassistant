"""Config flow for the Meraki Home Assistant integration."""

<<<<<<< HEAD
<<<<<<< HEAD
from __future__ import annotations

import logging
from typing import Any

<<<<<<< HEAD
<<<<<<< HEAD
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
=======
=======
>>>>>>> 08ff23a4 (fix(config_flow): Resolve CI failures by correcting test logic)
=======
<<<<<<< HEAD
from __future__ import annotations

=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import logging
from typing import Any

import voluptuous as vol
<<<<<<< HEAD
<<<<<<< HEAD
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
=======
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 498e2557 (fix(config_flow): Remove unused voluptuous import)
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow

from .authentication import validate_meraki_credentials
from .const import (
    CONF_INTEGRATION_TITLE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .options_flow import MerakiOptionsFlowHandler
from .schemas import CONFIG_SCHEMA, OPTIONS_SCHEMA

_LOGGER = logging.getLogger(__name__)


<<<<<<< HEAD
<<<<<<< HEAD
@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlowHandler(config_entries.ConfigFlow):
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
=======
<<<<<<< HEAD
@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlowHandler(config_entries.ConfigFlow):
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
class MerakiConfigFlow(ConfigFlow, domain="meraki_ha"):  # type: ignore[call-arg]
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = "cloud_poll"
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}
        self.options: dict[str, Any] = {}

    async def async_step_user(
<<<<<<< HEAD
<<<<<<< HEAD
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle the initial step.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
<<<<<<< HEAD
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle the initial step.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                validation_result = await validate_meraki_credentials(
                    self.hass,
                    user_input[CONF_MERAKI_API_KEY],
                    user_input[CONF_MERAKI_ORG_ID],
                )
                self.data[CONF_MERAKI_API_KEY] = user_input[CONF_MERAKI_API_KEY]
                self.data[CONF_MERAKI_ORG_ID] = user_input[CONF_MERAKI_ORG_ID]
                self.data["org_name"] = validation_result.get(
<<<<<<< HEAD
<<<<<<< HEAD
                    "org_name",
                    user_input[CONF_MERAKI_ORG_ID],
=======
<<<<<<< HEAD
                    "org_name",
                    user_input[CONF_MERAKI_ORG_ID],
=======
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
                )

                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                self._abort_if_unique_id_configured()

<<<<<<< HEAD
<<<<<<< HEAD
                # Show the general form by default
=======
<<<<<<< HEAD
                # Show the general form by default
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
                return await self.async_step_init()

            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
<<<<<<< HEAD
<<<<<<< HEAD
            except AbortFlow as e:
                raise e
=======
<<<<<<< HEAD
            except AbortFlow as e:
                raise e
=======
            except AbortFlow:
                return self.async_abort(reason="already_configured")
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
            except AbortFlow:
                return self.async_abort(reason="already_configured")
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
<<<<<<< HEAD
<<<<<<< HEAD
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
=======
<<<<<<< HEAD
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle the general settings step.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        )

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
<<<<<<< HEAD
        """
        Handle the general settings step.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
        """Handle the general settings step."""
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.data.get("org_name", CONF_INTEGRATION_TITLE),
                data=self.data,
                options=self.options,
            )

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        return self.async_show_form(
            step_id="init",
            data_schema=OPTIONS_SCHEMA,
        )
<<<<<<< HEAD
=======

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """
        Get the options flow for this handler.

        Args:
        ----
            config_entry: The config entry.

        Returns
        -------
            The options flow handler.

        """
        return MerakiOptionsFlowHandler(config_entry)

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Handle a reconfiguration flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """
        Get the options flow for this handler.

        Args:
        ----
            config_entry: The config entry.

        Returns
        -------
            The options flow handler.

        """
        return MerakiOptionsFlowHandler(config_entry)

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
<<<<<<< HEAD
        """
        Handle a reconfiguration flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
=======
        """Handle a reconfiguration flow."""
<<<<<<< HEAD
        from .meraki_data_coordinator import MerakiDataCoordinator

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 1025a183 (fix: Resolve config flow error during reconfiguration)
=======
>>>>>>> 498e2557 (fix(config_flow): Remove unused voluptuous import)
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if not entry:
            return self.async_abort(reason="unknown_entry")

        if user_input is not None:
            new_options = {**entry.options, **user_input}
            self.hass.config_entries.async_update_entry(entry, options=new_options)
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA,
            entry.options,
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema_with_defaults,
        )

    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
    ) -> vol.Schema:
        """
        Populate a schema with default values from a dictionary.

        Args:
        ----
            schema: The schema to populate.
            defaults: The default values.

        Returns
        -------
            The populated schema.

        """
        new_schema_keys = {}
        for key, value in schema.schema.items():
            if key.schema in defaults:
                new_key = type(key)(key.schema, default=defaults[key.schema])
                new_schema_keys[new_key] = value
            else:
                new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
=======
<<<<<<< HEAD
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, entry.options
            ),
        )
>>>>>>> 00a5566c (fix: Resolve CI failures in config flow and dependencies)
=======
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA, entry.options
=======
=======
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][entry.entry_id][
            "coordinator"
        ]
        network_options = []
        if coordinator.data and coordinator.data.get("networks"):
            network_options = [
                {"label": network["name"], "value": network["id"]}
                for network in coordinator.data["networks"]
            ]

        schema_with_defaults = MerakiOptionsFlowHandler._populate_schema_defaults(
            OPTIONS_SCHEMA, entry.options, network_options
>>>>>>> 1025a183 (fix: Resolve config flow error during reconfiguration)
=======
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA, entry.options
>>>>>>> 498e2557 (fix(config_flow): Remove unused voluptuous import)
        )

        return self.async_show_form(
            step_id="reconfigure", data_schema=schema_with_defaults
        )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 498e2557 (fix(config_flow): Remove unused voluptuous import)

    def _populate_schema_defaults(
        self, schema: vol.Schema, defaults: dict[str, Any]
    ) -> vol.Schema:
        """Populate a schema with default values from a dictionary."""
        new_schema_keys = {}
        for key, value in schema.schema.items():
            if key.schema in defaults:
                new_key = type(key)(key.schema, default=defaults[key.schema])
                new_schema_keys[new_key] = value
            else:
                new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
<<<<<<< HEAD
>>>>>>> b654416b (fix(tests): Address PR feedback)
=======
>>>>>>> 1025a183 (fix: Resolve config flow error during reconfiguration)
=======
>>>>>>> 498e2557 (fix(config_flow): Remove unused voluptuous import)
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
