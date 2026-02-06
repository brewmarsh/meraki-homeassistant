"""Options flow for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .const_conf import CONF_INTEGRATION_TITLE
from .coordinator import MerakiDataUpdateCoordinator
from .helpers.schema import get_filtered_schema, populate_schema_defaults
from .schemas import (
    OPTIONS_SCHEMA_ADVANCED,
    OPTIONS_SCHEMA_CAMERAS,
    OPTIONS_SCHEMA_GENERAL,
    OPTIONS_SCHEMA_SENSORS,
)


class MerakiOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for the Meraki integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.options = dict(config_entry.options)
        self._coordinator_instance: MerakiDataUpdateCoordinator | None = None

    @property
    def coordinator(self) -> MerakiDataUpdateCoordinator:
        """Get the coordinator."""
        if self._coordinator_instance is None:
            self._coordinator_instance = self.hass.data[DOMAIN][
                self.config_entry.entry_id
            ]["coordinator"]
        return self._coordinator_instance

    def _get_network_options(self) -> list[dict[str, str]]:
        """Get network options."""
        network_options = []
        if self.coordinator.data and self.coordinator.data.get("networks"):
            for network in self.coordinator.data["networks"]:
                name = getattr(network, "name", None)
                if name is None and isinstance(network, dict):
                    name = network.get("name")

                net_id = getattr(network, "id", None)
                if net_id is None and isinstance(network, dict):
                    net_id = network.get("id")

                if name and net_id:
                    network_options.append({"label": name, "value": net_id})
        return network_options

    def _has_cameras(self) -> bool:
        """Check if cameras are present."""
        devices = self.coordinator.data.get("devices", [])
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
                return True
        return False

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage the options flow menu."""
        menu_options = ["general", "sensors"]
        if self._has_cameras():
            menu_options.append("cameras")
        menu_options.append("advanced")

        return self.async_show_menu(step_id="init", menu_options=menu_options)

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage general settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema = populate_schema_defaults(
            OPTIONS_SCHEMA_GENERAL,
            self.options,
            self._get_network_options(),
        )
        return self.async_show_form(step_id="general", data_schema=schema)

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage sensor settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        schema = populate_schema_defaults(
            OPTIONS_SCHEMA_SENSORS,
            self.options,
        )
        return self.async_show_form(step_id="sensors", data_schema=schema)

    async def async_step_cameras(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage camera settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        # Filter schema in case we somehow got here without cameras
        # (though menu handles it)
        # But also get_filtered_schema handles filtering specific options if needed.
        filtered_schema = get_filtered_schema(
            self.coordinator.data.get("devices", []),
            OPTIONS_SCHEMA_CAMERAS,
        )

        schema = populate_schema_defaults(
            filtered_schema,
            self.options,
        )
        return self.async_show_form(step_id="cameras", data_schema=schema)

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage advanced settings."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=CONF_INTEGRATION_TITLE, data=self.options
            )

        filtered_schema = get_filtered_schema(
            self.coordinator.data.get("devices", []),
            OPTIONS_SCHEMA_ADVANCED,
        )

        schema = populate_schema_defaults(
            filtered_schema,
            self.options,
        )
        return self.async_show_form(step_id="advanced", data_schema=schema)
