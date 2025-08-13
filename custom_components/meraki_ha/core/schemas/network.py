"""Schemas for network-related API responses."""

import voluptuous as vol

NETWORK_SCHEMA = vol.Schema(
    {
        vol.Required("id"): str,
        vol.Required("name"): str,
        vol.Required("productTypes"): [str],
        vol.Optional("timeZone"): str,
        vol.Optional("tags"): [str],
        vol.Optional("isBoundToConfigTemplate"): bool,
        vol.Optional("notes"): str,
        vol.Optional("url"): str,
        vol.Optional("organizationId"): str,
    }
)
