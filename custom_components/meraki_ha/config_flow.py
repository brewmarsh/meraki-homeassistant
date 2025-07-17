"""Config flow for the Meraki Home Assistant integration.

This module defines the configuration flow for setting up and managing
the Meraki integration within Home Assistant. It handles user input for
API keys, organization IDs, and other configuration options.
"""

import logging
import traceback
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector

from ..authentication import validate_meraki_credentials
from .api.meraki_api import MerakiAPIClient
from ..const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    # CONF_RELAXED_TAG_MATCHING, # Removed as it's no longer used or defined
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha config_flow.py loaded")

# Schema for the initial user configuration step
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
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
            except Exception as e:  # pylint: disable=broad-except
                # Catch any other unexpected errors during the process.
                _LOGGER.error("An unexpected error occurred during config flow: %s", e)
                # Log the full traceback for debugging.
                _LOGGER.error(traceback.format_exc())
                errors["base"] = "unknown"  # Generic error key for UI
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
        data_schema_with_options = CONFIG_SCHEMA.extend(
            {
                # Scan interval field: integer, required, with a default value.
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=user_input.get(  # Pre-fill
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): int,
                # Device name format field: optional, dropdown selector.
                vol.Optional(
                    "device_name_format",
                    default=user_input.get("device_name_format", "omitted"),  # Pre-fill
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[  # Dropdown options
                            {"value": "prefix", "label": "Prefix"},
                            {"value": "suffix", "label": "Suffix"},
                            {"value": "omitted", "label": "Omitted"},
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                # CONF_RELAXED_TAG_MATCHING was removed here.
            }
        )
        # Note: UI descriptions for fields like CONF_SCAN_INTERVAL can be
        # added directly in the schema or, more commonly, handled via the
        # strings.json translation files for localization.

        # Show the configuration form to the user.
        # `step_id` refers to this current step ("user").
        # `data_schema` defines the form fields.
        # `errors` will display any validation errors from the previous
        # submission attempt.
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema_with_options,
            errors=errors,
        )

    async def async_step_reauth(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle reauthentication for the Meraki integration.

        This step is triggered if the existing credentials become invalid.
        It prompts the user to re-enter their API key and Organization ID.

        Args:
            user_input: Optional dictionary of user input for reauthentication.
                When not None, it is expected to contain:
                - CONF_MERAKI_API_KEY (str): The new Meraki API key.
                - CONF_MERAKI_ORG_ID (str): The new Meraki Organization ID.

        Returns:
            A FlowResult object representing the next step in the reauth flow. This could be
            showing the form again with errors, or aborting if reauth is successful.
        """
        _LOGGER.debug("Meraki HA: async_step_reauth called")
        errors: Dict[str, str] = {}

        # This block executes if the user has submitted new credentials for
        # reauthentication.
        if user_input is not None:
            _LOGGER.debug("Reauth user input received: %s", user_input)
            try:
                # Step 1: Validate the newly provided credentials.
                await validate_meraki_credentials(
                    user_input[CONF_MERAKI_API_KEY],
                    user_input[CONF_MERAKI_ORG_ID],
                )

                # Step 2: Get the existing config entry that needs
                # reauthentication. The `entry_id` is typically passed in
                # `self.context`.
                existing_entry = self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
                if not existing_entry:
                    # This case should ideally not happen if the reauth flow
                    # is triggered correctly.
                    return self.async_abort(reason="unknown_entry")

                # Step 3: Update the existing config entry's data with the new
                # credentials. Options are typically not changed during reauth,
                # only the core authentication data.
                updated_data: Dict[str, Any] = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                }

                self.hass.config_entries.async_update_entry(
                    existing_entry, data=updated_data
                )  # Only update data, options remain.
                # Step 4: Reload the config entry to apply the new credentials.
                await self.hass.config_entries.async_reload(existing_entry.entry_id)
                _LOGGER.info("Meraki reauthentication successful.")
                # Abort the reauth flow with a "reauth_successful" reason.
                return self.async_abort(reason="reauth_successful")

            # Handle specific exceptions during reauthentication.
            except ConfigEntryAuthFailed:
                _LOGGER.warning("Reauthentication failed: Invalid credentials.")
                errors["base"] = "invalid_auth"
            except ValueError:  # From validate_meraki_credentials
                _LOGGER.warning("Reauthentication failed: Invalid Organization ID.")
                errors["base"] = "invalid_org_id"
            except aiohttp.ClientError:
                _LOGGER.error("Reauthentication failed: Cannot connect to Meraki API.")
                errors["base"] = "cannot_connect"
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.error("An unexpected error occurred during reauth: %s", e)
                _LOGGER.error(traceback.format_exc())
                errors["base"] = "unknown"

        # Show the reauthentication form to the user.
        # This form typically only asks for the credentials that need
        # revalidation (API Key, Org ID).
        # `CONFIG_SCHEMA` is used here, which defines these core fields.
        return self.async_show_form(
            step_id="reauth", data_schema=CONFIG_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle a reconfiguration flow."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry

        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                options={
                    **entry.options,
                    "scan_interval": user_input["scan_interval"],
                    "device_name_format": user_input["device_name_format"],
                },
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "scan_interval",
                        default=entry.options.get(
                            "scan_interval", DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                    vol.Optional(
                        "device_name_format",
                        default=entry.options.get("device_name_format", "omitted"),
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
                }
            ),
        )

    # This method seems to be for dynamically setting the title of the
    # config entry, but it's not directly called by the config flow steps.
    # It might be used by HA UI when displaying existing config entries.
    def async_config_entry_title(self, data: Dict[str, Any]) -> str:
        """Return a dynamic title for the config entry.

        Args:
            data: The config entry data dictionary, typically `config_entry.data`.
                  Expected to contain `CONF_MERAKI_ORG_ID`.

        Returns:
            The desired title string for the config entry.
        """
        # Create a user-friendly title using the Organization ID.
        # Default title if org_id is somehow missing.
        org_id = data.get(CONF_MERAKI_ORG_ID, "Meraki Cloud")
        return f"Meraki: {org_id}"

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "OptionsFlowHandler":
        """Get the options flow for this handler.

        This function is called by Home Assistant when the user wants to configure
        the options for an existing Meraki integration instance.

        Args:
            config_entry: The config entry for which to get the options flow.

        Returns:
            An instance of the OptionsFlowHandler, which manages the options UI.
        """
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration.

    This class allows users to modify integration options (like scan interval,
    device name format) after the initial setup.
    """
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the options flow initialization.

        This step shows a form to the user with current options and allows modification.
        If user_input is provided, it means the user has submitted the form.

        Args:
            user_input: Optional dictionary of user input from the options form.
                When not None, it may contain:
                - CONF_SCAN_INTERVAL (int): The desired scan interval.
                - "device_name_format" (str): The chosen device name format.
                Current values from `self.config_entry.options` are used as defaults in the form.

        Returns:
            A FlowResult object, either showing the options form or creating/updating
            the config entry's options and finishing the flow.
        """
        # This block executes if the user has submitted the options form.
        if user_input is not None:
            _LOGGER.debug("Options flow user input: %s", user_input)
            # Validate and process the scan interval.
            try:
                # Ensure scan_interval is an integer.
                scan_interval_input = user_input.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                )
                user_input[CONF_SCAN_INTERVAL] = int(scan_interval_input)
                # Enforce a minimum scan interval (e.g., > 0).
                if user_input[CONF_SCAN_INTERVAL] <= 0:
                    # Reset to default if an invalid value (e.g., zero or
                    # negative) is entered.
                    user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL
            except ValueError:
                # Handle cases where conversion to int fails.
                _LOGGER.warning(
                    "Invalid scan interval provided: %s. Defaulting to %s.",
                    user_input.get(CONF_SCAN_INTERVAL),
                    DEFAULT_SCAN_INTERVAL,
                )
                user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

            # Create an entry with the updated options.
            # The 'title' for an options flow entry is usually empty.
            # 'data' here refers to the options data.
            return self.async_create_entry(title="", data=user_input)

        # This block executes if showing the options form for the first time.
        # Define the schema for the options form, pre-filling with current
        # option values.
        options_schema = vol.Schema(
            {
                # Scan interval field, defaulting to current value or global
                # default.
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(  # Current option value
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): int,
                # Device name format field, dropdown selector.
                vol.Optional(
                    "device_name_format",
                    default=self.config_entry.options.get(
                        "device_name_format", "omitted"  # Default if not set
                    ),
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
                # CONF_RELAXED_TAG_MATCHING was removed here.
            }
        )
        # Note: UI descriptions for these options fields are typically handled
        # via the strings.json translation files for better localization and
        # maintainability.

        # Show the options form to the user.
        return self.async_show_form(step_id="init", data_schema=options_schema)
