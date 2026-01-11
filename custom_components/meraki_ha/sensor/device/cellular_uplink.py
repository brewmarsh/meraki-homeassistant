"""Sensor entity for Meraki Cellular Gateway uplink status."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...helpers.logging_helper import MerakiLoggers
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.SENSOR


class MerakiCellularUplinkSensor(
    CoordinatorEntity,
    SensorEntity,  # type: ignore[type-arg]
):
    """Representation of a Meraki Cellular Gateway Uplink sensor."""

    coordinator: MerakiDataCoordinator
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Mapping[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Cellular Uplink sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_cellular_uplink"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
        )
        self.entity_description = SensorEntityDescription(
            key="cellular_uplink",
            name="Cellular Status",
            icon="mdi:signal-cellular-3",
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _get_primary_uplink(self) -> dict[str, Any] | None:
        """Get the primary cellular uplink data."""
        device = self._get_current_device_data()
        if not device:
            return None
        uplinks = device.get("cellular_uplinks", [])
        if uplinks and isinstance(uplinks, list):
            # Return the first (primary) uplink
            return uplinks[0] if uplinks else None
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state from coordinator data."""
        uplink = self._get_primary_uplink()

        if not uplink:
            self._attr_native_value = "unknown"
            self._attr_icon = "mdi:signal-cellular-outline"
            self._attr_extra_state_attributes = {}
            return

        # Status is the main value
        self._attr_native_value = uplink.get("status", "unknown")

        # Set icon based on connection type
        connection_type = uplink.get("connectionType", "").lower()
        if "5g" in connection_type:
            self._attr_icon = "mdi:signal-5g"
        elif "4g" in connection_type or "lte" in connection_type:
            self._attr_icon = "mdi:signal-4g"
        elif "3g" in connection_type:
            self._attr_icon = "mdi:signal-3g"
        else:
            self._attr_icon = "mdi:signal-cellular-3"

        # Get signal stats
        signal_stat = uplink.get("signalStat")
        rsrp = signal_stat.get("rsrp") if signal_stat else None
        rsrq = signal_stat.get("rsrq") if signal_stat else None

        roaming = uplink.get("roaming")
        roaming_status = roaming.get("status") if roaming else None

        attributes = {
            "provider": uplink.get("provider"),
            "connection_type": uplink.get("connectionType"),
            "signal_type": uplink.get("signalType"),
            "public_ip": uplink.get("publicIp"),
            "ip": uplink.get("ip"),
            "rsrp": rsrp,
            "rsrq": rsrq,
            "apn": uplink.get("apn"),
            "iccid": uplink.get("iccid"),
            "roaming_status": roaming_status,
            "interface": uplink.get("interface"),
        }
        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available:
            return False
        return self._get_current_device_data() is not None


class MerakiCellularSignalSensor(
    CoordinatorEntity,
    SensorEntity,  # type: ignore[type-arg]
):
    """Representation of a Meraki Cellular Gateway Signal Strength sensor."""

    coordinator: MerakiDataCoordinator
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Mapping[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Cellular Signal sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_cellular_signal"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
        )
        self.entity_description = SensorEntityDescription(
            key="cellular_signal",
            name="Signal Strength (RSRP)",
            device_class=SensorDeviceClass.SIGNAL_STRENGTH,
            native_unit_of_measurement="dBm",
            icon="mdi:signal",
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _get_primary_uplink(self) -> dict[str, Any] | None:
        """Get the primary cellular uplink data."""
        device = self._get_current_device_data()
        if not device:
            return None
        uplinks = device.get("cellular_uplinks", [])
        if uplinks and isinstance(uplinks, list):
            return uplinks[0] if uplinks else None
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state from coordinator data."""
        uplink = self._get_primary_uplink()

        if not uplink:
            self._attr_native_value = None
            return

        signal_stat = uplink.get("signalStat", {})
        rsrp = signal_stat.get("rsrp")

        # RSRP is often returned as a string, convert to int
        if rsrp is not None:
            try:
                self._attr_native_value = int(rsrp)
            except (ValueError, TypeError):
                self._attr_native_value = None
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available:
            return False
        device = self._get_current_device_data()
        if not device:
            return False
        uplinks = device.get("cellular_uplinks", [])
        return bool(uplinks)
