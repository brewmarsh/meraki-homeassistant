"""Config flow for the Meraki Home Assistant integration."""

<<<<<<< HEAD
from __future__ import annotations

=======
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
import logging
from typing import Any

import voluptuous as vol
<<<<<<< HEAD
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
=======
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow

from .authentication import validate_meraki_credentials
from .const import (
    CONF_INTEGRATION_TITLE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
<<<<<<< HEAD
    DOMAIN,
=======
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
)
from .core.errors import MerakiAuthenticationError, MerakiConnectionError
from .options_flow import MerakiOptionsFlowHandler
from .schemas import CONFIG_SCHEMA, OPTIONS_SCHEMA

_LOGGER = logging.getLogger(__name__)


<<<<<<< HEAD
@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlowHandler(config_entries.ConfigFlow):
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
=======
class MerakiConfigFlow(ConfigFlow, domain="meraki_ha"):  # type: ignore[call-arg]
    """Handle a config flow for Meraki."""

    VERSION = 1
    CONNECTION_CLASS = "cloud_poll"
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}
        self.options: dict[str, Any] = {}

    async def async_step_user(
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
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
                    "org_name",
                    user_input[CONF_MERAKI_ORG_ID],
=======
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
                )

                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                self._abort_if_unique_id_configured()

<<<<<<< HEAD
                # Show the general form by default
=======
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
                return await self.async_step_init()

            except MerakiAuthenticationError:
                errors["base"] = "invalid_auth"
            except MerakiConnectionError:
                errors["base"] = "cannot_connect"
<<<<<<< HEAD
            except AbortFlow as e:
                raise e
=======
            except AbortFlow:
                return self.async_abort(reason="already_configured")
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
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
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the general settings step."""
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=self.data.get("org_name", CONF_INTEGRATION_TITLE),
                data=self.data,
                options=self.options,
            )

<<<<<<< HEAD
        return self.async_show_form(
            step_id="init",
            data_schema=OPTIONS_SCHEMA,
        )

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
        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return MerakiOptionsFlowHandler(config_entry)

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a reconfiguration flow."""
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if not entry:
            return self.async_abort(reason="unknown_entry")

        if user_input is not None:
            new_options = {**entry.options, **user_input}
            self.hass.config_entries.async_update_entry(entry, options=new_options)
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_abort(reason="reconfigure_successful")

        schema_with_defaults = self._populate_schema_defaults(
<<<<<<< HEAD
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
=======
            OPTIONS_SCHEMA, entry.options
        )

        return self.async_show_form(
            step_id="reconfigure", data_schema=schema_with_defaults
        )

    def _populate_schema_defaults(
        self, schema: vol.Schema, defaults: dict[str, Any]
    ) -> vol.Schema:
        """Populate a schema with default values from a dictionary."""
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        new_schema_keys = {}
        for key, value in schema.schema.items():
            if key.schema in defaults:
                new_key = type(key)(key.schema, default=defaults[key.schema])
                new_schema_keys[new_key] = value
            else:
                new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
