"""Sensor entity representing the client count of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinators import MerakiMainCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDClientCountSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Client Count sensor."""

    entity_description = SensorEntityDescription(
        key="client_count",
        name="client count",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="clients",
    )

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "clientCount")
        self._update_client_count()

    @callback
    def _update_client_count(self) -> None:
        """Update the client count from coordinator data."""
        ssid_data = self._get_current_ssid_data()
        if ssid_data and "clientCount" in ssid_data:
            self._attr_native_value = ssid_data["clientCount"]
        elif self.coordinator.data and "clients" in self.coordinator.data:
            # Fallback to manual calculation if clientCount not in ssid_data
            all_clients = self.coordinator.data.get("clients", [])
            ssid_name = (
                ssid_data.get("name")
                if ssid_data
                else self._ssid_data_at_init.get("name")
            )
            if not ssid_name:
                self._attr_native_value = 0
                return

            self._attr_native_value = sum(
                1
                for client in all_clients
                if client.get("networkId") == self._network_id
                and client.get("ssid") == ssid_name
                and str(client.get("status", "")).lower() == "online"
            )
        else:
            self._attr_native_value = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_client_count()
        self.async_write_ha_state()
