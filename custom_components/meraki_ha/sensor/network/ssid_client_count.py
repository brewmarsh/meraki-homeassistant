"""Sensor entity representing the client count of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
<<<<<<< HEAD
<<<<<<< HEAD
=======
from homeassistant.core import callback
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from homeassistant.core import callback
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDClientCountSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Client Count sensor."""

    entity_description = SensorEntityDescription(
        key="client_count",
        name="Client Count",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="clients",
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "clientCount")
<<<<<<< HEAD
<<<<<<< HEAD
        self._attr_native_value = self._ssid_data_at_init.get("clientCount")
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        # Initialize to 0, will be updated via _handle_coordinator_update
        self._attr_native_value = 0
        self._update_client_count()

    @callback
    def _update_client_count(self) -> None:
        """Calculate and update the client count."""
        if not self.coordinator.data:
            self._attr_native_value = 0
            return

        all_clients = self.coordinator.data.get("clients", [])
        if not all_clients:
            self._attr_native_value = 0
            return

        # Find the SSID name (since clients refer to SSID by name)
        current_ssid_data = self._get_current_ssid_data()
        if not current_ssid_data:
            # Fallback to initial data if current not found (unlikely)
            ssid_name = self._ssid_data_at_init.get("name")
        else:
            ssid_name = current_ssid_data.get("name")

        if not ssid_name:
            self._attr_native_value = 0
            return

        count = sum(
            1
            for client in all_clients
            if client.get("networkId") == self._network_id
            and client.get("ssid") == ssid_name
            and str(client.get("status", "")).lower() == "online"
        )
        self._attr_native_value = count

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_client_count()
        self.async_write_ha_state()
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
