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
    """Handle a config or options flow for meraki_ha."""

    config_flow = {}
    OPTIONS_FLOW = True

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
                device_name_format = user_input.get("device_name_format", "omitted")
                relaxed_tag_matching = user_input.get(CONF_RELAXED_TAG_MATCHING, False)

                data = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                }

                options = {
                    CONF_SCAN_INTERVAL: scan_interval,
                    "device_name_format": device_name_format,
                    CONF_RELAXED_TAG_MATCHING: relaxed_tag_matching,
                }

                _LOGGER.debug(f"User input before create entry: {data}, {options}")
                return self.async_create_entry(
                    data=data,
                    options=options,
                    title="Meraki Cloud Integration",
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
                vol.Optional(CONF_RELAXED_TAG_MATCHING, default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema_with_scan, errors=errors
        )

    async def async_step_reauth(self, user_input=None):
        """Handle reauthentication."""
        _LOGGER.debug("Meraki HA: async_step_reauth in config_flow.py called")
        errors: Dict[str, str] = {}
        if user_input is not None:
            _LOGGER.debug(f"Reauth User input: {user_input}")
            try:
                existing_entry = self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
                updated_data = {
                    CONF_MERAKI_API_KEY: user_input[CONF_MERAKI_API_KEY],
                    CONF_MERAKI_ORG_ID: user_input[CONF_MERAKI_ORG_ID],
                }

                updated_options = {
                    CONF_SCAN_INTERVAL: existing_entry.options[CONF_SCAN_INTERVAL],
                    "device_name_format": existing_entry.options["device_name_format"],
                    CONF_RELAXED_TAG_MATCHING: existing_entry.options[
                        CONF_RELAXED_TAG_MATCHING
                    ],
                }

                self.hass.config_entries.async_update_entry(
                    existing_entry, data=updated_data, options=updated_options
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

    def async_config_entry_title(self, data: Dict[str, Any]) -> str:
        """Return config entry title."""
        return "Meraki Cloud Integration"

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manage the options flow initialization."""
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
                            ]
                        )
                    ),
                    vol.Optional(
                        CONF_RELAXED_TAG_MATCHING,
                        default=self.config_entry.options.get(
                            CONF_RELAXED_TAG_MATCHING, False
                        ),
                    ): bool,
                }
            ),
        )
