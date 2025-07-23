"""Config flow for the Meraki Home Assistant integration.

This module defines the configuration flow for setting up and managing
the Meraki integration within Home Assistant. It handles user input for
API keys, organization IDs, and other configuration options.
"""

import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector

from .reconfigure_flow import async_step_reconfigure
from .authentication import validate_meraki_credentials
from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .reauth_flow import async_step_reauth
from .options_flow import OptionsFlowHandler
from .schemas import CONFIG_SCHEMA

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha config_flow.py loaded")


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlowHandler(config_entries.ConfigFlow):
    """Handle a config or options flow for the Meraki integration."""

    VERSION = 1
    # Remove config_flow and OPTIONS_FLOW if not used or handled by
    # inheritance
    # config_flow = {}  # This seems unused
    # OPTIONS_FLOW = True  # Implicitly True if async_get_options_flow defined

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the initial step of the config flow (user setup).

        This step prompts the user for their Meraki API key and Organization ID.
        It validates these credentials and creates a config entry if valid.

        Args:
            user_input: Optional dictionary of user input. When not None, it is expected
                to contain:
                - CONF_MERAKI_API_KEY (str): The Meraki API key.
                - CONF_MERAKI_ORG_ID (str): The Meraki Organization ID.
                - CONF_SCAN_INTERVAL (int): The scan interval in seconds.
                - "device_name_format" (str): One of "prefix", "suffix", "omitted".
                Defaults are applied if optional fields are missing.

        Returns:
            A FlowResult object representing the next step in the config flow. This could be
            showing the form again with errors, or creating the config entry and finishing.
        """
        _LOGGER.debug("Meraki HA: async_step_user called")
        errors: Dict[str, str] = {}

        # This block executes if the user has submitted input (not the first
        # time showing the form).
        if user_input is not None:
            _LOGGER.debug("User input received: %s", user_input)
            try:
                # Step 1: Validate the provided Meraki API credentials.
                # This involves making an actual API call to Meraki to confirm
                # the key and org ID are valid.
                validation_result = await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY],
                    user_input[CONF_MERAKI_ORG_ID],
                )
                # Use fetched org_name for the title, fallback to Org ID if name couldn't be fetched.
                org_name = validation_result.get(
                    "org_name", user_input[CONF_MERAKI_ORG_ID]
                )

                # Step 2: If credentials are valid, prepare the data and
                # options for the config entry. 'data' usually stores
                # information that doesn't change often (like API keys).
                data: Dict[str, Any] = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                }
                # 'options' usually stores user-configurable settings that can
                # be changed later.
                options: Dict[str, Any] = {
                    CONF_SCAN_INTERVAL: user_input.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),  # Use default if not provided
                    "device_name_format": user_input.get(
                        "device_name_format", "omitted"
                    ),  # Default device name format
                }

                _LOGGER.debug(
                    "Creating config entry with data: %s, options: %s",
                    data,
                    options,
                )
                # Step 3: Set a unique ID for this config entry to prevent
                # duplicate entries for the same Meraki organization.
                # This helps Home Assistant manage existing configurations.
                await self.async_set_unique_id(user_input[CONF_MERAKI_ORG_ID])
                # Abort if a config entry with this unique ID already exists.
                self._abort_if_unique_id_configured()

                # Step 4: Create the config entry with the validated data and
                # options. The title is what users will see in the
                # integrations list.
                return self.async_create_entry(
                    title=f"{org_name} [{user_input[CONF_MERAKI_ORG_ID]}]",
                    data=data,
                    options=options,
                )

            # Handle specific exceptions that can occur during the validation
            # process.
            except ConfigEntryAuthFailed:
                # Authentication failed (e.g., invalid API key).
                _LOGGER.warning("Authentication failed with provided credentials.")
                from .repairs import async_create_api_key_issue

                await async_create_api_key_issue(self.hass, self.context["entry_id"])
                errors["base"] = "invalid_auth"  # Error key for UI message
            except ValueError:
                # Invalid organization ID (e.g., not found for the given API
                # key).
                _LOGGER.warning("Invalid Organization ID provided.")
                errors["base"] = "invalid_org_id"  # Error key for UI
            except aiohttp.ClientError:
                # Connection error (e.g., cannot reach Meraki API).
                _LOGGER.error("Cannot connect to Meraki API.")
                errors["base"] = "cannot_connect"  # Error key for UI
            except Exception as e:
                _LOGGER.error("An unexpected error occurred during config flow: %s", e)
                errors["base"] = "unknown"
        else:
            # This block executes if user_input is None (first time showing
            # the form).
            # Initialize user_input as an empty dict to prevent errors when
            # accessing it for defaults.
            user_input = {}

        # Define the schema for the user input form.
        # This schema includes fields for API key, Org ID, and other options like scan interval.
        # `CONFIG_SCHEMA` provides the base (API Key, Org ID).
        # `.extend` adds more fields to this base schema for the form.
        data_schema = CONFIG_SCHEMA.extend({
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            ): int,
            vol.Optional(
                "device_name_format",
                default=user_input.get("device_name_format", "omitted")
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "prefix", "label": "Prefix"},
                        {"value": "suffix", "label": "Suffix"},
                        {"value": "omitted", "label": "Omitted"},
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        })

        # Show the configuration form to the user.
        # `step_id` refers to this current step ("user").
        # `data_schema` defines the form fields.
        # `errors` will display any validation errors from the previous
        # submission attempt.
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_reauth(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle reauthentication for the Meraki integration."""
        return await async_step_reauth(self, user_input)

    async def async_step_reconfigure(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle a reconfiguration flow."""
        return await async_step_reconfigure(self, user_input)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "OptionsFlowHandler":
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)
