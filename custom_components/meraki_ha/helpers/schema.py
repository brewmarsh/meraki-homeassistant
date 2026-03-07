"""Schema helper for the Meraki integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const.integration import (
    (,
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    ),
)


def get_filtered_schema(
    devices: list[Any],
    base_schema: vol.Schema,
) -> vol.Schema:
    """
    Filter schema based on discovered hardware.

    Args:
    ----
        devices: List of discovered devices.
        base_schema: The base schema to filter.

    Returns
    -------
        The filtered schema.

    """
    has_cameras = False
    has_switches = False

    for device in devices:
        p_type = ""
        model = ""
        if isinstance(device, dict):
            p_type = device.get("productType") or device.get("product_type", "")
            model = device.get("model", "")
        else:
            p_type = getattr(device, "product_type", "") or ""
            model = getattr(device, "model", "") or ""

        if "camera" in p_type.lower() or (model and model.startswith("MV")):
            has_cameras = True
        if "switch" in p_type.lower() or (model and model.startswith("MS")):
            has_switches = True

    filtered_schema_dict = {}
    for key, value in base_schema.schema.items():
        if key.schema == CONF_ENABLE_CAMERA_ENTITIES and not has_cameras:
            continue
        if key.schema == CONF_ENABLE_CAMERA_SENSE and not has_cameras:
            continue
        if key.schema == CONF_ENABLE_VLAN_MANAGEMENT and not has_switches:
            continue
        filtered_schema_dict[key] = value

    return vol.Schema(filtered_schema_dict)


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
            new_config["options"] = network_options  # type: ignore[typeddict-item]
            value = selector.SelectSelector(new_config)

        new_schema_keys[key] = value
    return vol.Schema(new_schema_keys)
