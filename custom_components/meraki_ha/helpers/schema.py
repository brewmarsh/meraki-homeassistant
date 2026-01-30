"""Schema helper for the Meraki integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const import CONF_IGNORED_NETWORKS


def populate_schema_defaults(
    schema: vol.Schema,
    defaults: dict[str, Any],
    network_options: list[dict[str, str]] | None = None,
) -> vol.Schema:
    """
    Populate a schema with default values.

    This is used to ensure that the options form is pre-filled with the
    existing values from the config entry.

    Args:
    ----
        schema: The schema to populate.
        defaults: The default values.
        network_options: The network options.

    Returns
    -------
        The populated schema.

    """
    new_schema_keys = {}
    for key, value in schema.schema.items():
        key_name = key.schema
        # 'key.schema' is the name of the option (e.g., 'scan_interval')
        if key_name in defaults:
            # Create a new voluptuous key (e.g., vol.Required) with the
            # default value set to the existing option value.
            key = type(key)(key.schema, default=defaults[key.schema])

        if (
            key_name == CONF_IGNORED_NETWORKS
            and isinstance(value, selector.SelectSelector)
            and network_options is not None
        ):
            new_config = value.config.copy()
            new_config["options"] = network_options
            value = selector.SelectSelector(new_config)

        new_schema_keys[key] = value
    return vol.Schema(new_schema_keys)
