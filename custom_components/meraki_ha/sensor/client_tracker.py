"""Sensor entities for tracking Meraki client count.

Note: Individual client tracking is now handled by the device_tracker
platform (device_tracker.py) using proper ScannerEntity implementation.
This module only provides the total client count sensor.
"""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..core.utils.naming_utils import format_device_name
from ..helpers.logging_helper import MerakiLoggers
from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.DEVICE_TRACKER

CLIENT_TRACKER_DEVICE_ID = "client_tracker"


class ClientTrackerDeviceSensor(CoordinatorEntity, SensorEntity):
    """A sensor that tracks the total number of connected clients.

    This sensor provides a count of all connected clients across the
    Meraki organization. Individual client presence tracking is handled
    by the device_tracker platform.
    """

    _attr_has_entity_name = True
    entity_description = SensorEntityDescription(
        key="client_tracker_total",
        name="Tracked Clients",
        icon="mdi:account-group",
    )

    def __init__(
        self, coordinator: MerakiDataCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor.

        Parameters
        ----------
        coordinator : MerakiDataCoordinator
            The data update coordinator.
        config_entry : ConfigEntry
            The config entry for this integration.

        """
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{CLIENT_TRACKER_DEVICE_ID}"

        tracker_device_data = {
            "name": "Client Tracker",
            "productType": "tracker",
        }
        formatted_name = format_device_name(
            device=tracker_device_data,
            config=self._config_entry.options,
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, CLIENT_TRACKER_DEVICE_ID)},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Client Tracker",
        )
        self._update_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if self.coordinator.data and self.coordinator.data.get("clients"):
            self._attr_native_value = len(self.coordinator.data["clients"])
        else:
            self._attr_native_value = 0
