"""Sensor entity for monitoring connected clients on a Meraki SSID."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_entity_name
from ...helpers.device_info_helpers import resolve_device_info
=======
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

_LOGGER = logging.getLogger(__name__)


class MerakiSsidConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki SSID Connected Clients sensor."""

    _attr_icon = "mdi:wifi-strength-4"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        network_id: str,
        ssid_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._network_id = network_id
        self._ssid_number = ssid_data["number"]
        self._config_entry = config_entry
        self._attr_unique_id = (
            f"{self._network_id}_{self._ssid_number}_connected_clients"
        )
<<<<<<< HEAD
        self._attr_name = "Connected clients"
=======
        self._attr_name = f"{ssid_data['name']} Connected Clients"
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

        self._attr_device_info = resolve_device_info(
            entity_data=ssid_data,
            config_entry=self._config_entry,
        )
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        all_clients = self.coordinator.data.get("clients", [])
<<<<<<< HEAD
        ssid = self.coordinator.get_ssid(self._network_id, self._ssid_number)
        ssid_name = ssid.get("name") if ssid else None

        if not ssid_name or not all_clients:
=======
        if not all_clients:
            self._attr_native_value = 0
            return

        ssid_name = None
        for ssid in self.coordinator.data.get("ssids", []):
            if (
                ssid.get("networkId") == self._network_id
                and ssid.get("number") == self._ssid_number
            ):
                ssid_name = ssid.get("name")
                break

        if not ssid_name:
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
            self._attr_native_value = 0
            return

        count = sum(
            1
            for client in all_clients
            if client.get("networkId") == self._network_id
            and client.get("ssid") == ssid_name
            and client.get("status") == "Online"
        )
        self._attr_native_value = count

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.coordinator.data is not None
