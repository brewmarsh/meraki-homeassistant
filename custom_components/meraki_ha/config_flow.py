"""Config flow for the Meraki Home Assistant integration."""

import importlib
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.core import callback

# Dynamically import ConfigFlowResult where needed
# from homeassistant.config_entries import ConfigFlowResult

_LOGGER = logging.getLogger(__name__)

# The ConfigFlowHandler class has been moved to config_flow_handler.py
# and will be imported dynamically when needed.


async def async_get_handler(hass: Any) -> Any:
    """Dynamically get the ConfigFlowHandler class."""
    config_flow_handler_module = importlib.import_module(
        "custom_components.meraki_ha.config_flow_handler"
    )
    return config_flow_handler_module.ConfigFlowHandler


async def async_step_user(
    hass: Any,
    init_step_data: dict[str, Any] | None = None,
) -> Any:  # Use Any for now, as ConfigFlowResult is dynamically imported
    """Handle the initial step."""
    # Dynamically import necessary modules and classes
    # ha_config_entries = importlib.import_module("homeassistant.config_entries")
    const = importlib.import_module(".const", "custom_components.meraki_ha")
    schemas = importlib.import_module(".schemas", "custom_components.meraki_ha")
    authentication = importlib.import_module(
        ".authentication", "custom_components.meraki_ha"
    )
    errors_module = importlib.import_module(
        ".core.errors", "custom_components.meraki_ha"
    )

    MerakiAuthenticationError = errors_module.MerakiAuthenticationError
    MerakiConnectionError = errors_module.MerakiConnectionError
    validate_meraki_credentials = authentication.validate_meraki_credentials

    errors: dict[str, str] = {}
    if init_step_data is not None:
        try:
            validation_result = await validate_meraki_credentials(
                hass,
                init_step_data[const.CONF_MERAKI_API_KEY],
                init_step_data[const.CONF_MERAKI_ORG_ID],
            )
            data = {
                const.CONF_MERAKI_API_KEY: init_step_data[const.CONF_MERAKI_API_KEY],
                const.CONF_MERAKI_ORG_ID: init_step_data[const.CONF_MERAKI_ORG_ID],
                "org_name": validation_result.get(
                    "org_name", init_step_data[const.CONF_MERAKI_ORG_ID]
                ),
            }

            handler = await async_get_handler(hass)
            instance = handler()
            instance.data = data

            await instance.async_set_unique_id(init_step_data[const.CONF_MERAKI_ORG_ID])
            instance._abort_if_unique_id_configured()

            return await instance.async_step_init(user_input=init_step_data)

        except MerakiAuthenticationError:
            errors["base"] = "invalid_auth"
        except MerakiConnectionError:
            errors["base"] = "cannot_connect"
        except AbortFlow as e:
            raise e
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

    handler = await async_get_handler(hass)
    instance = handler()
    return instance.async_show_form(
        step_id="user",
        data_schema=schemas.CONFIG_SCHEMA,
        errors=errors,
    )


async def async_step_init(
    hass: Any,
    init_step_data: dict[str, Any] | None = None,
) -> Any:  # Use Any for now, as ConfigFlowResult is dynamically imported
    """Handle the general settings step."""
    handler = await async_get_handler(hass)
    instance = handler()

    # Dynamically import necessary modules
    schemas = importlib.import_module(".schemas", "custom_components.meraki_ha")
    const = importlib.import_module(".const", "custom_components.meraki_ha")
    # ha_config_entries = importlib.import_module("homeassistant.config_entries")
    # ConfigFlowResult = ha_config_entries.ConfigFlowResult

    if init_step_data is not None:
        instance.options.update(init_step_data)
        return instance.async_create_entry(
            title=instance.data.get("org_name", const.CONF_INTEGRATION_TITLE),
            data=instance.data,
            options=instance.options,
        )

    return instance.async_show_form(
        step_id="init",
        data_schema=schemas.OPTIONS_SCHEMA,
    )


@callback
def async_get_options_flow(
    config_entry: ConfigEntry,
) -> OptionsFlow:
    """Get the options flow for this handler."""
    # Dynamically import options flow handler
    options_flow_handler_module = importlib.import_module(
        ".options_flow", "custom_components.meraki_ha"
    )
    return options_flow_handler_module.MerakiOptionsFlowHandler(config_entry)


async def async_step_reconfigure(
    hass: Any,
    context: dict | None = None,
    user_input: dict[str, Any] | None = None,
) -> Any:  # Use Any for now, as ConfigFlowResult is dynamically imported
    """Handle a reconfiguration flow."""
    # Dynamically import necessary modules
    # ha_config_entries = importlib.import_module("homeassistant.config_entries")
    schemas = importlib.import_module(".schemas", "custom_components.meraki_ha")

    handler_class = await async_get_handler(hass)
    instance = handler_class()
    instance.context = context if context else {}

    entry = hass.config_entries.async_get_entry(instance.context["entry_id"])
    if not entry:
        return instance.async_abort(reason="unknown_entry")

    if user_input is not None:
        new_options = {**entry.options, **user_input}
        hass.config_entries.async_update_entry(entry, options=new_options)
        await hass.config_entries.async_reload(entry.entry_id)
        return instance.async_abort(reason="reconfigure_successful")

    schema_with_defaults = instance._populate_schema_defaults(
        schemas.OPTIONS_SCHEMA,
        entry.options,
    )

    return instance.async_show_form(
        step_id="reconfigure",
        data_schema=schema_with_defaults,
    )


# Note: _populate_schema_defaults is a method of ConfigFlowHandler,
# so it needs to be called on an instance of the handler.
# If _populate_schema_defaults is needed outside of an instance,
# it might need to be a static method or moved to a utility function.
# Adjustments may be needed depending on how this method is used.
