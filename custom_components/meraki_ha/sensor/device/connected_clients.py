"""Sensor entity for monitoring connected clients on a Meraki device."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from dataclasses import asdict

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Connected Clients sensor."""

    _attr_icon = "mdi:account-network"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_connected_clients"
        self._attr_name = "Connected Clients"

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
        )
        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)

    @callback
    def _update_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        device = self._get_current_device_data()
        if not device:
            self._attr_native_value = 0
            return

        product_type = device.product_type

        # For routers (appliances), the client count is all online clients
        # in the network.
        if product_type in ["appliance", "cellularGateway"]:
            network_id = device.network_id
            all_clients = self.coordinator.data.get("clients", [])
            if not all_clients:
                self._attr_native_value = 0
                return

            network_clients = [
                c
                for c in all_clients
                if c.get("networkId") == network_id and c.get("status") == "Online"
            ]
            self._attr_native_value = len(network_clients)
        # For other devices (switches, APs), use the direct per-device client list.
        else:
            clients_by_serial = self.coordinator.data.get("clients_by_serial", {})
            device_clients = clients_by_serial.get(self._device_serial)

            if device_clients is None:
                # Data for this specific device might not be available yet
                self._attr_native_value = 0
                return

            self._attr_native_value = len(device_clients)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
