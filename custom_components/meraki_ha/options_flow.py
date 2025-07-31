"""Options flow for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL

from .const import (
    CONF_DEVICE_NAME_FORMAT,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEFAULT_SCAN_INTERVAL,
    DEVICE_NAME_FORMAT_OPTIONS,
)
from .schemas import RECONFIGURE_SCHEMA

_LOGGER = logging.getLogger(__name__)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the options flow initialization."""
        if user_input is not None:
            _LOGGER.debug("Options flow user input: %s", user_input)
            try:
                scan_interval_input = user_input.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                )
                user_input[CONF_SCAN_INTERVAL] = int(scan_interval_input)
                if user_input[CONF_SCAN_INTERVAL] <= 0:
                    user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL
            except ValueError:
                _LOGGER.warning(
                    "Invalid scan interval provided: %s. Defaulting to %s.",
                    user_input.get(CONF_SCAN_INTERVAL),
                    DEFAULT_SCAN_INTERVAL,
                )
                user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                    vol.Optional(
                        CONF_DEVICE_NAME_FORMAT,
                        default=self.config_entry.options.get(
                            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
                        ),
                    ): vol.In(DEVICE_NAME_FORMAT_OPTIONS),
                }
            ),
        )
