"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector

from .const import (
    CONF_ENABLED_NETWORKS,
    CONF_FILTER_SSID,
    CONF_FILTER_VLAN,
    CONF_INTEGRATION_TITLE,
    DOMAIN,
)
from .schemas import OPTIONS_SCHEMA


class MerakiOptionsFlowHandler(OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """
        Initialize options flow.

        Args:
        ----
            config_entry: The config entry.

        """
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Manage the options flow.

        Args:
        ----
            user_input: The user input.

        Returns
        -------
            The flow result.

        """
        from .meraki_data_coordinator import MerakiDataCoordinator

        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE,
                data=self.options,
            )

        coordinator: MerakiDataCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]["coordinator"]

        network_options = []
        vlan_options = []
        ssid_options = []

        if coordinator.data:
            networks_by_id = {
                network["id"]: network
                for network in coordinator.data.get("networks", [])
            }

            if networks_by_id:
                network_options = [
                    {"label": network["name"], "value": network["id"]}
                    for network in networks_by_id.values()
                ]

            vlans_by_network = coordinator.data.get("vlans", {})
            for network_id, vlans in vlans_by_network.items():
                if network := networks_by_id.get(network_id):
                    if isinstance(vlans, list):
                        for vlan in vlans:
                            vlan_options.append(
                                {
                                    "label": f"{network['name']} - {vlan.get('name', 'Unnamed VLAN')} ({vlan['id']})",
                                    "value": vlan["id"],
                                }
                            )

            ssids = coordinator.data.get("ssids", [])
            for ssid in ssids:
                if network := networks_by_id.get(ssid.get("networkId")):
                    ssid_options.append(
                        {
                            "label": f"{network['name']} - {ssid['name']}",
                            "value": ssid["name"],
                        }
                    )

        # Populate the form with existing values from the config entry.
        schema_with_defaults = self._populate_schema_defaults(
            OPTIONS_SCHEMA, self.options, network_options, vlan_options, ssid_options
        )

        return self.async_show_form(step_id="init", data_schema=schema_with_defaults)

    def _populate_schema_defaults(
        self,
        schema: vol.Schema,
        defaults: dict[str, Any],
        network_options: list[dict[str, str]],
        vlan_options: list[dict[str, str]],
        ssid_options: list[dict[str, str]],
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
            vlan_options: The VLAN options.
            ssid_options: The SSID options.

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

            if key_name == CONF_ENABLED_NETWORKS and isinstance(
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = network_options
                value = selector.SelectSelector(new_config)

            if key_name == CONF_FILTER_VLAN and isinstance(
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = vlan_options
                value = selector.SelectSelector(new_config)

            if key_name == CONF_FILTER_SSID and isinstance(
                value, selector.SelectSelector
            ):
                new_config = value.config.copy()
                new_config["options"] = ssid_options
                value = selector.SelectSelector(new_config)

            new_schema_keys[key] = value
        return vol.Schema(new_schema_keys)
