"""Sensor entity for monitoring connected clients on a Meraki device."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceConnectedClientsSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki Connected Clients sensor."""

    _attr_icon = "mdi:account-network"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_connected_clients"
        self._attr_name = "Connected Clients"

        self._attr_device_info = resolve_device_info(
            entity_data=device_data,
            config_entry=self._config_entry,
        )
        self._update_state()

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _update_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        device = self._get_current_device_data()
        if not device:
            self._attr_native_value = 0
            return

        product_type = device.get("productType")
        network_id = device.get("networkId")
        all_clients = self.coordinator.data.get("clients", [])
        count = 0

        if not all_clients:
            self._attr_native_value = 0
            return

        # Filter clients for the current device's network
        network_clients = [
            c
            for c in all_clients
            if c.get("networkId") == network_id and c.get("status") == "Online"
        ]

        if product_type == "wireless":
            count = sum(
                1
                for client in network_clients
                if client.get("recentDeviceSerial") == self._device_serial
            )
        elif product_type == "switch":
            count = sum(
                1
                for client in network_clients
                if client.get("recentDeviceConnection") == "Wired"
            )
        elif product_type == "appliance":
            count = len(network_clients)

        self._attr_native_value = count

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
