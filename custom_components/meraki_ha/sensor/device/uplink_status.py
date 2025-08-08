"""Sensor entity for representing the uplink status of a Meraki MX appliance."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)

STATE_UNAVAILABLE_UPLINK = "Unavailable"
STATE_UNKNOWN_UPLINK = "Unknown"


class MerakiUplinkStatusSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki MX Appliance Uplink Status sensor."""

    _attr_icon = "mdi:upload-network-outline"
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
        self._attr_unique_id = f"{self._device_serial}_uplink_status"
        self._attr_name = "Uplink Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            sw_version=device_data.get("firmware"),
        )
        self._attr_extra_state_attributes: Dict[str, Any] = {}
        self._update_state()

    def _get_current_device_data(self) -> Dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    def _get_uplink_status(self, device_data: Dict[str, Any]) -> str:
        """Get the status of the primary uplink for this device."""
        if not device_data or "uplinks" not in device_data:
            return STATE_UNAVAILABLE_UPLINK

        uplinks = device_data.get("uplinks", [])
        if not uplinks:
            return "offline"

        active_uplink = any(u.get("status") == "active" for u in uplinks)
        ready_uplink = any(u.get("status") == "ready" for u in uplinks)

        if active_uplink:
            return "online"
        if ready_uplink:
            return "ready"

        return "offline"

    @callback
    def _update_state(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_info = self._get_current_device_data()

        if not current_device_info:
            self._attr_native_value = STATE_UNAVAILABLE_UPLINK
            self._attr_extra_state_attributes = {}
            return

        self._attr_native_value = self._get_uplink_status(current_device_info)

        current_attributes = {
            "lan_ip": current_device_info.get("lanIp"),
            "tags": current_device_info.get("tags", []),
            "network_id": current_device_info.get("networkId"),
        }

        for uplink in current_device_info.get("uplinks", []):
            interface = uplink.get("interface", "unknown_interface")
            current_attributes[f"{interface}_status"] = uplink.get("status")
            current_attributes[f"{interface}_ip"] = uplink.get("ip")
            current_attributes[f"{interface}_gateway"] = uplink.get("gateway")
            current_attributes[f"{interface}_public_ip"] = uplink.get("publicIp")
            current_attributes[f"{interface}_dns_servers"] = uplink.get("dns")

        self._attr_extra_state_attributes = {
            k: v for k, v in current_attributes.items() if v is not None
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
