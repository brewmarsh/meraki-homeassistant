"""Config flow for the meraki_ha integration."""

import logging
import traceback
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    CONF_RELAXED_TAG_MATCHING,  # add this line
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha config_flow.py loaded")  # Added Log

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for meraki_ha."""

    config_flow = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the initial step of the config flow."""
        _LOGGER.debug("Meraki HA: async_step_user in config_flow.py called")
        errors: Dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"User input: {user_input}")
            try:
                scan_interval = user_input.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                )
                device_name_format = user_input.get(
                    "device_name_format", "omitted"
                )  # Get the new option
                relaxed_tag_matching = user_input.get(
                    CONF_RELAXED_TAG_MATCHING, False
                )  # Get relaxed tag matching

                merged_data = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                    CONF_SCAN_INTERVAL: scan_interval,
                    "device_name_format": device_name_format,  # Add the new option to merged data
                    CONF_RELAXED_TAG_MATCHING: relaxed_tag_matching,  # add this line
                }
                _LOGGER.debug(f"User input before create entry: {merged_data}")
                # Removed unique_id for compatibility
                return self.async_create_entry(
                    data=merged_data,
                )

            except ConfigEntryAuthFailed:
                errors["base"] = "invalid_auth"
            except ValueError:
                errors["base"] = "invalid_org_id"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error(f"Config flow error: {e}")
                _LOGGER.error(traceback.format_exc())
                errors["base"] = "unknown"
        else:
            user_input = {}

        data_schema_with_scan = CONFIG_SCHEMA.extend(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=DEFAULT_SCAN_INTERVAL,
                    description={
                        "suggested_value": DEFAULT_SCAN_INTERVAL,
                        "description": "Enter the scan interval in minutes. Shorter intervals increase API usage.",
                    },
                ): int,
                vol.Optional(
                    "device_name_format", default="omitted"
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": "prefix", "label": "Prefix"},
                            {"value": "suffix", "label": "Suffix"},
                            {"value": "omitted", "label": "Omitted"},
                        ],
                    )
                ),
                vol.Optional(
                    CONF_RELAXED_TAG_MATCHING, default=False
                ): bool,  # add this line
            }
        )

        self.config_flow = {"user": SchemaFlowFormStep(data_schema_with_scan)}

        return self.async_show_form(
            step_id="user", data_schema=data_schema_with_scan, errors=errors
        )

    async def async_step_reauth(self, user_input=None):
        """Handle reauthentication."""
        _LOGGER.debug(
            "Meraki HA: async_step_reauth in config_flow.py called"
        )  # added log
        errors: Dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"Reauth User input: {user_input}")
            try:
                existing_entry = self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
                self.hass.config_entries.async_update_entry(
                    existing_entry, data=user_input
                )
                await self.hass.config_entries.async_reload(existing_entry.entry_id)
                _LOGGER.info("Meraki reauthentication successful.")
                return self.async_abort(reason="reauth_successful")
            except ConfigEntryAuthFailed:
                errors["base"] = "invalid_auth"
            except ValueError:
                errors["base"] = "invalid_org_id"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error(f"Reauth Config flow error: {e}")
                _LOGGER.error(traceback.format_exc())
                errors["base"] = "unknown"
        return self.async_show_form(
            step_id="reauth", data_schema=CONFIG_SCHEMA, errors=errors
        )

    def async_config_entry_title(self, options: Dict[str, Any]) -> str:
        """Return config entry title.

        Args:
            options: Configuration options.

        Returns:
            The config entry title.
        """
        return "Meraki Cloud Integration"


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Meraki integration."""

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manage the options flow initialization.

        Args:
            user_input: User input from the form.

        Returns:
            A dictionary with the next step of the flow.
        """
        if user_input is not None:
            return self.async_create_entry(title="Meraki Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                        description={
                            "suggested_value": DEFAULT_SCAN_INTERVAL,
                            "description": "Enter the scan interval in minutes. Shorter intervals increase API usage.",
                        },
                    ): int,
                    vol.Optional(
                        "device_name_format",
                        default=self.config_entry.options.get(
                            "device_name_format", "omitted"
                        ),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                {"value": "prefix", "label": "Prefix"},
                                {"value": "suffix", "label": "Suffix"},
                                {"value": "omitted", "label": "Omitted"},
                            ],
                        )
                    ),
                    vol.Optional(
                        CONF_RELAXED_TAG_MATCHING,
                        default=self.config_entry.options.get(
                            CONF_RELAXED_TAG_MATCHING, False
                        ),
                    ): bool,  # add this line
                }
            ),
        )
