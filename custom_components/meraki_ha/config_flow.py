"""Configuration flow for the Meraki Home Assistant integration.

This module implements the configuration flow (for initial setup) and
options flow (for changing settings after setup) for the Meraki integration.
It handles user input for API key, organization ID, and other settings,
validates credentials, and creates/updates the configuration entry.
"""

import logging
import traceback
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector
from homeassistant.core import callback

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    CONF_RELAXED_TAG_MATCHING,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha config_flow.py loaded")

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handles the configuration flow for the Meraki integration.

    This class manages the steps a user takes to set up the Meraki integration,
    including providing API credentials and initial configuration options.
    It also handles re-authentication if credentials become invalid.

    The `VERSION` attribute indicates the version of the config flow.
    If you change the schema or steps, you might need to increment this.
    `MINOR_VERSION` can be used for smaller, compatible changes.
    """

    VERSION = 1
    #MINOR_VERSION = 1 # Example if you had minor changes

    # config_flow and OPTIONS_FLOW are class attributes used by Home Assistant.
    # config_flow seems unused here, OPTIONS_FLOW = True is incorrect for main config flow.
    # This should likely be ConnectionStrategy = config_entries.CONN_STRATEGY_POLL or similar if applicable.
    # For options flow, it's defined on the OptionsFlowHandler.

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handles the initial user setup step.

        This step prompts the user for their Meraki API key, Organization ID,
        and other initial settings like scan interval and device name formatting.
        It validates the credentials and creates a config entry if successful.

        Args:
            user_input (Optional[Dict[str, Any]]): A dictionary containing the
                user's input from the form. None if the form is being displayed
                for the first time.

        Returns:
            config_entries.FlowResult: The result of the step, which can be a form
                to show to the user, an abort message, or a config entry creation signal.
        """
        _LOGGER.debug("Meraki HA: Starting async_step_user in config_flow.")
        errors: Dict[str, str] = {}

        if user_input is not None:
            _LOGGER.debug("User input received: %s", user_input)
            try:
                # Attempt to validate credentials before creating the entry.
                # This requires the `validate_meraki_credentials` function.
                from .authentication import validate_meraki_credentials

                api_key = user_input[CONF_MERAKI_API_KEY]
                org_id = user_input[CONF_MERAKI_ORG_ID]

                # Perform validation (example, actual validation might be more complex)
                # This should ideally happen before async_create_entry.
                # If validate_meraki_credentials raises exceptions, they will be caught below.
                await validate_meraki_credentials(api_key, org_id)
                _LOGGER.info("Meraki credentials successfully validated.")


                # Prepare data and options for the config entry.
                # Core connection data (API key, Org ID) goes into `data`.
                data_for_entry = {
                    CONF_MERAKI_API_KEY: api_key,
                    CONF_MERAKI_ORG_ID: org_id,
                }

                # Other settings (scan interval, formatting) go into `options`.
                options_for_entry = {
                    CONF_SCAN_INTERVAL: user_input.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                    "device_name_format": user_input.get(
                        "device_name_format", "omitted"
                    ),
                    CONF_RELAXED_TAG_MATCHING: user_input.get(
                        CONF_RELAXED_TAG_MATCHING, False
                    ),
                }

                _LOGGER.debug(
                    "Creating config entry with data: %s, options: %s",
                    data_for_entry,
                    options_for_entry,
                )
                # Title for the config entry, can be dynamic (e.g., Org Name).
                # For now, using a static title.
                # Consider fetching Org Name during validation to use here.
                return self.async_create_entry(
                    title="Meraki Cloud Integration", # Consider using Org Name if fetched
                    data=data_for_entry,
                    options=options_for_entry,
                )

            except ConfigEntryAuthFailed:
                _LOGGER.warning("Authentication failed: Invalid API key.")
                errors["base"] = "invalid_auth"
            except ValueError as ve: # Specific for invalid Org ID from our validation
                _LOGGER.warning("Invalid Organization ID: %s", ve)
                errors["base"] = "invalid_org_id"
            except aiohttp.ClientError:
                _LOGGER.error("Cannot connect to Meraki API.")
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("An unknown error occurred during config flow.")
                errors["base"] = "unknown"
        # else:
            # If user_input is None, we are showing the form for the first time.
            # user_input = {} # No need to re-initialize, it's already None or populated.

        # Define the schema for the user input form, including advanced options.
        # This schema is shown if user_input is None or if there were errors.
        form_schema = vol.Schema(
            {
                vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.PASSWORD
                    )
                ),
                vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
                vol.Required(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): int, # Using simple int selector for now.
                        # For description, consider custom form or localization.
                vol.Optional(
                    "device_name_format", default="omitted"
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": "prefix", "label": "Prefix ([Type] Name)"},
                            {"value": "suffix", "label": "Suffix (Name [Type])"},
                            {"value": "omitted", "label": "Omitted (Name)"},
                        ],
                        mode=selector.SelectMode.DROPDOWN, # Or LIST
                    )
                ),
                vol.Optional(
                    CONF_RELAXED_TAG_MATCHING, default=False
                ): bool, # Boolean selector (checkbox)
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=form_schema, errors=errors
        )

    async def async_step_reauth(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handles the re-authentication flow.

        This step is triggered if the integration reports an authentication failure
        (e.g., API key becomes invalid). It prompts the user to re-enter their
        API key and Organization ID.

        Args:
            user_input (Optional[Dict[str, Any]]): User's input from the re-auth form.

        Returns:
            config_entries.FlowResult: The result of the re-authentication attempt.
        """
        _LOGGER.debug("Meraki HA: Starting async_step_reauth.")
        errors: Dict[str, str] = {}

        existing_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        if not existing_entry:
            return self.async_abort(reason="reauth_failed_missing_entry")


        if user_input is not None:
            _LOGGER.debug("Re-authentication input received: %s", user_input)
            try:
                from .authentication import validate_meraki_credentials

                api_key = user_input[CONF_MERAKI_API_KEY]
                org_id = user_input[CONF_MERAKI_ORG_ID]

                # Validate the new credentials.
                await validate_meraki_credentials(api_key, org_id)
                _LOGGER.info("Meraki re-authentication successful.")

                # Update the existing config entry with the new credentials.
                # Options are preserved from the existing entry.
                self.hass.config_entries.async_update_entry(
                    existing_entry,
                    data={
                        CONF_MERAKI_API_KEY: api_key,
                        CONF_MERAKI_ORG_ID: org_id,
                    },
                    # Options are typically not changed during re-auth, but preserved.
                    # options=existing_entry.options.copy(), # This line is implicitly handled by not passing options
                )
                # Reload the config entry to apply the new credentials.
                await self.hass.config_entries.async_reload(existing_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

            except ConfigEntryAuthFailed:
                _LOGGER.warning("Re-authentication failed: Invalid API key.")
                errors["base"] = "invalid_auth"
            except ValueError as ve: # Specific for invalid Org ID
                _LOGGER.warning("Re-authentication failed: Invalid Organization ID: %s", ve)
                errors["base"] = "invalid_org_id"
            except aiohttp.ClientError:
                _LOGGER.error("Cannot connect to Meraki API during re-authentication.")
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("An unknown error occurred during re-authentication.")
                errors["base"] = "unknown"

        # Schema for the re-authentication form (API key and Org ID only).
        reauth_schema = vol.Schema(
            {
                vol.Required(
                    CONF_MERAKI_API_KEY,
                    default=existing_entry.data.get(CONF_MERAKI_API_KEY, ""),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.PASSWORD
                    )
                ),
                vol.Required(
                    CONF_MERAKI_ORG_ID,
                    default=existing_entry.data.get(CONF_MERAKI_ORG_ID, ""),
                ): selector.TextSelector(),
            }
        )

        return self.async_show_form(
            step_id="reauth",
            data_schema=reauth_schema,
            errors=errors,
            description_placeholders={ # Pass current Org ID to description if needed
                "org_id": existing_entry.data.get(CONF_MERAKI_ORG_ID, "current")
            }
        )

    # async_config_entry_title is not a standard method in ConfigFlow.
    # The title is usually set during async_create_entry.
    # If this was intended for dynamically setting the title of an existing entry,
    # that's handled differently (e.g., via unique_id or other listeners).
    # For now, commenting out as it's not standard.
    # def async_config_entry_title(self, data: Dict[str, Any]) -> str:
    #     """Return config entry title."""
    #     # This method is not standard. Title is set in async_create_entry.
    #     # If you need to update title of existing entry, it's usually done via other means.
    #     return "Meraki Cloud Integration"

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "OptionsFlowHandler":
        """Get the options flow for this handler.

        This function is called by Home Assistant to obtain an instance of the
        options flow handler, allowing users to modify settings after the
        initial setup.

        Args:
            config_entry (config_entries.ConfigEntry): The config entry for which
                the options flow is being initiated.

        Returns:
            OptionsFlowHandler: An instance of the options flow handler.
        """
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handles the options flow for the Meraki integration.

    This class allows users to modify settings of an already configured
    Meraki integration instance, such as the scan interval or device
    name formatting.
    """

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initializes the options flow handler.

        Args:
            config_entry (config_entries.ConfigEntry): The config entry whose
                options are being modified. This entry contains the current
                option values.
        """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manages the initialization of the options flow.

        This step displays a form to the user with the current option values
        and allows them to modify these settings. Upon submission, it updates
        the config entry's options.

        Args:
            user_input (Optional[Dict[str, Any]]): A dictionary containing the
                user's input from the options form. None if the form is being
                displayed for the first time.

        Returns:
            config_entries.FlowResult: The result of the step, which can be a form
                to show to the user or an options entry creation signal.
        """
        if user_input is not None:
            # User has submitted new options.
            _LOGGER.debug("Updating Meraki options with user input: %s", user_input)
            # `async_create_entry` with an empty title and the new data effectively
            # updates the options for the existing config entry.
            return self.async_create_entry(title="", data=user_input)

        # Show the options form, pre-filled with current values.
        options_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): int, # Simple integer input for scan interval.
                        # Descriptions for form fields are better handled via localization strings.
                vol.Optional(
                    "device_name_format",
                    default=self.config_entry.options.get(
                        "device_name_format", "omitted" # Default to "omitted" if not set
                    ),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": "prefix", "label": "Prefix ([Type] Name)"},
                            {"value": "suffix", "label": "Suffix (Name [Type])"},
                            {"value": "omitted", "label": "Omitted (Name Only)"},
                        ],
                        mode=selector.SelectMode.DROPDOWN,
                    )
                ),
                vol.Optional(
                    CONF_RELAXED_TAG_MATCHING,
                    default=self.config_entry.options.get(
                        CONF_RELAXED_TAG_MATCHING, False # Default to False
                    ),
                ): bool, # Checkbox for boolean option.
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
