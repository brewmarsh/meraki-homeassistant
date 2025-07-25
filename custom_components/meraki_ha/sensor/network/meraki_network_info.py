"""Sensor for Meraki Device Network Information."""

import logging
from typing import Any, Dict  # List removed

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Network Information Sensor."""

    _attr_icon = "mdi:information-outline"
    _attr_has_entity_name = True  # Home Assistant will prepend the device name

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._network_id: str = network_data.get("id", "")
        self._attr_unique_id = f"{self._network_id}_network_info"
        # self.entity_id = f"sensor.{DOMAIN}_{self._network_id}_network_info" # Let HA generate

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._network_id)},
            name=network_data.get("name"),
            # No other fields like name, model, manufacturer, sw_version.
            # These should be inherited from the device entry already created by MerakiDataUpdateCoordinator.
        )
        # The sensor's friendly name suffix
        self._attr_name = "Network Information"

        self._attr_extra_state_attributes: Dict[str, Any] = {}
        # Initialize state
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        if not self.coordinator.data:
            self._attr_native_value = "Unknown"
            self._attr_extra_state_attributes = {}
            return

        networks = self.coordinator.data.get("networks", [])
        if not networks:
            self._attr_native_value = "Unknown"
            self._attr_extra_state_attributes = {}
            _LOGGER.debug("No networks found in coordinator data")
            return

        current_network_data = None
        for network in networks:
            if network.get("id") == self._network_id:
                current_network_data = network
                break
        for network in networks:
            if network.get("id") == self._network_id:
                current_network_data = network
                break

        if current_network_data:
            self._attr_native_value = current_network_data.get("name", self._network_id)

            attributes = {
                "hostname": current_network_data.get("name"),
                "notes": current_network_data.get("notes"),
                "network_id": self._network_id,
                "organization_id": current_network_data.get("organizationId"),
                "product_types": current_network_data.get("productTypes"),
                "tags": current_network_data.get("tags", []),
                "time_zone": current_network_data.get("timeZone"),
                "url": current_network_data.get("url"),
            }
            self._attr_extra_state_attributes = {
                k: v for k, v in attributes.items() if v is not None
            }

        # _LOGGER.debug(
        #     "Network Info Sensor update for %s: state=%s, attributes=%s",
        #     self._device_serial,
        #     self._attr_native_value,
        #     self._attr_extra_state_attributes,
        # ) # Removed

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False
        if not self.coordinator.data or not self.coordinator.data.get("networks"):
            return False
        # Check if the specific device data is available
        for network in self.coordinator.data["networks"]:
            if network.get("id") == self._network_id:
                return True
        return False
