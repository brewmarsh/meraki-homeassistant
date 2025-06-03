"""Sensor for Meraki Device Network Information."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Device Network Information Sensor."""

    _attr_icon = "mdi:information-outline"
    _attr_has_entity_name = True  # Home Assistant will prepend the device name

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_network_info"
        # self.entity_id = f"sensor.{DOMAIN}_{self._device_serial}_network_info" # Let HA generate

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=device_data.get("name"), # This is the device name for the DeviceInfo
            manufacturer="Cisco Meraki",
            model=device_data.get("model"),
        )
        # The sensor's friendly name suffix
        self._attr_name = "Network Information"

        self._attr_extra_state_attributes: Dict[str, Any] = {}
        # Initialize state
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data: Optional[Dict[str, Any]] = None
        if (
            self.coordinator.data
            and self.coordinator.data.get("devices")
            and isinstance(self.coordinator.data["devices"], list)
        ):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    current_device_data = device
                    break
        
        if self._device_serial == "Q3FA-PJD8-PUDP":
            _LOGGER.info(
                "MERAKI_NETINFO_SENSOR_DATA for %s: %s",
                self._device_serial,
                current_device_data
            )

        if not current_device_data:
            self._attr_native_value = "Unknown"
            self._attr_extra_state_attributes = {}
            _LOGGER.debug(
                "Device %s not found in coordinator data for network info sensor.",
                self._device_serial
            )
            return

        # The state of this sensor will be the device's reported name or serial
        self._attr_native_value = current_device_data.get("name", self._device_serial)

        attributes = {
            "hostname": current_device_data.get("name"),
            "serial_number": current_device_data.get("serial"),
            "model": current_device_data.get("model"),
            "mac_address": current_device_data.get("mac"), # Added MAC address
            "wan1_ip_address": current_device_data.get("wan1Ip"),
            "wan1_dns_servers": current_device_data.get("wan1_dns_servers", []),
            "wan2_ip_address": current_device_data.get("wan2Ip"),
            "wan2_dns_servers": current_device_data.get("wan2_dns_servers", []),
            "lan_ip_address": current_device_data.get("lanIp"),
            "public_ip_address": current_device_data.get("publicIp"),
            "network_id": current_device_data.get("networkId"), # Added Network ID
            "tags": current_device_data.get("tags", []),
            "firmware_version": current_device_data.get("firmware"), # Added firmware from base device data
            "firmware_up_to_date": current_device_data.get("firmware_up_to_date"), # From data fetcher
            "latest_firmware_version": current_device_data.get("latest_firmware_version"), # From data fetcher
            "lan_dns_settings": current_device_data.get("lan_dns_settings"), # LAN DNS settings from fetcher
        }
        
        # Filter out attributes with None values to keep it clean
        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }
        
        _LOGGER.debug(
            "Network Info Sensor update for %s: state=%s, attributes=%s",
            self._device_serial,
            self._attr_native_value,
            self._attr_extra_state_attributes
        )

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
        if not self.coordinator.data or not self.coordinator.data.get("devices"):
            return False
        # Check if the specific device data is available
        for device in self.coordinator.data["devices"]:
            if device.get("serial") == self._device_serial:
                return True
        return False
