"""Binary sensor for Meraki switch port status."""

from collections.abc import Mapping
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..helpers.device_info_helpers import resolve_device_info
from ..helpers.entity_helpers import get_device_from_coordinator
from ..helpers.logging_helper import MerakiLoggers
from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.SENSOR


class SwitchPortSensor(CoordinatorEntity, BinarySensorEntity):  # type: ignore[type-arg]
    """Representation of a Meraki switch port sensor."""

    coordinator: MerakiDataCoordinator
    _attr_state_color = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Mapping[str, Any],
        port: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._attr_unique_id = f"{self._device['serial']}_{self._port['portId']}"
        self._attr_name = f"Port {self._port['portId']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        if self.coordinator.config_entry is None:
            return None
        return resolve_device_info(self._device, self.coordinator.config_entry)

    def _get_current_port_data(self) -> dict[str, Any] | None:
        """Get the current port data from the coordinator."""
        device = get_device_from_coordinator(self.coordinator, self._device["serial"])
        if not device:
            return None
        for port in device.get("ports_statuses", []):
            if port.get("portId") == self._port.get("portId"):
                return port
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device = get_device_from_coordinator(self.coordinator, self._device["serial"])
        if device:
            self._device = device
            current_port = self._get_current_port_data()
            if current_port:
                self._port = current_port
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self._get_current_port_data() is not None

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        return port.get("status") == "Connected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        poe_data = port.get("poe", {}) if isinstance(port.get("poe"), dict) else {}
        usage_data = (
            port.get("usageInKb", {}) if isinstance(port.get("usageInKb"), dict) else {}
        )
        traffic_data = (
            port.get("trafficInKbps", {})
            if isinstance(port.get("trafficInKbps"), dict)
            else {}
        )

        attrs = {
            "port_id": port.get("portId"),
            "speed": port.get("speed"),
            "duplex": port.get("duplex"),
            "vlan": port.get("vlan"),
            "enabled": port.get("enabled"),
            # Client info (from port status API)
            "client_name": port.get("clientName"),
            "client_mac": port.get("clientMac"),
            "client_count": port.get("clientCount"),
            # PoE info
            "poe_enabled": poe_data.get("enabled"),
            "poe_allocated": poe_data.get("isAllocated"),
            "power_usage_wh": port.get("powerUsageInWh"),
            # Traffic stats
            "usage_total_kb": usage_data.get("total"),
            "traffic_kbps": traffic_data.get("total"),
            # LLDP/CDP neighbor info
            "lldp_system_name": (
                port.get("lldp", {}).get("systemName")
                if isinstance(port.get("lldp"), dict)
                else None
            ),
            "cdp_device_id": (
                port.get("cdp", {}).get("deviceId")
                if isinstance(port.get("cdp"), dict)
                else None
            ),
        }

        # Add coordinator update timestamp
        if self.coordinator.last_successful_update:
            attrs["last_meraki_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )

        # Filter out None values for cleaner attributes
        return {k: v for k, v in attrs.items() if v is not None}
