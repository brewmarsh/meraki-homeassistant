"""Helper functions for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.helpers import selector

from .const import CONF_IGNORED_NETWORKS


def populate_schema_defaults(
    schema: vol.Schema,
    defaults: dict[str, Any],
    network_options: list[dict[str, str]] | None = None,
) -> vol.Schema:
    """
    Populate a schema with default values from a dictionary.

    Args:
    ----
        schema: The schema to populate.
        defaults: The default values.
        network_options: A list of network options for the ignored networks selector.

    Returns:
    -------
        The populated schema.

    """
    new_schema_keys = {}
    for key, value in schema.schema.items():
        key_name = key.schema
        if key_name in defaults:
            key = type(key)(key.schema, default=defaults[key_name])

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
