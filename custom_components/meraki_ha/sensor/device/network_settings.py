"""Sensors for Meraki device network settings."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.typing import StateType

from ...coordinators import MerakiMainCoordinator
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceUplinkBaseSensor(MerakiEntity, SensorEntity):
    """Base class for Meraki Device Uplink sensors."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self._interface = interface

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
        )

    def _get_uplink_data(self) -> dict[str, Any] | None:
        """Retrieve the latest uplink data from the coordinator."""
        device = self.coordinator.get_device(self._device_serial)
        if device and device.uplinks:
            for uplink in device.uplinks:
                if uplink.get("interface") == self._interface:
                    return uplink
        return None

    def _truncate_value(self, value: str | None) -> str | None:
        """Abbreviate long IPv6 addresses for UI display."""
        if not value:
            return value

        def truncate_ip(ip: str) -> str:
            """Truncate a single IP if it is a long IPv6 address."""
            if ":" in ip:
                blocks = ip.split(":")
                if len(blocks) > 4:
                    return f"{blocks[0]}:{blocks[1]}...{blocks[-2]}:{blocks[-1]}"
            return ip

        # Handle comma-separated lists (e.g., DNS)
        if "," in value:
            return ", ".join(truncate_ip(v.strip()) for v in value.split(","))

        return truncate_ip(value)


class MerakiDeviceIPSensor(MerakiDeviceUplinkBaseSensor):
    """Sensor for Meraki device IP address."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        name: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_data, config_entry, interface)

        # Clean up interface name for display (e.g., lanIp -> LAN, publicIp -> Public)
        display_interface = interface.replace("Ip", "").replace("IP", "")
        if not display_interface: # for "ip" or "IP" interfaces
             display_interface = "IP"
        else:
             display_interface = display_interface.upper()

        self.entity_description = SensorEntityDescription(
            key=f"{interface}_ip",
            name=name or f"{display_interface} IP",
            icon="mdi:ip-network",
        )
        self._attr_name = cast(str | None, self.entity_description.name)
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        device = self.coordinator.get_device(self._device_serial)
        ip_value: str | None = None

        if self._interface == "lanIp" and device:
            if device.model and device.model.startswith("MT"):
                self._attr_native_value = "N/A (Bluetooth)"
                self._attr_extra_state_attributes = {}
                return
            lan_ip = device.lan_ip
            if (
                (not lan_ip)
                and device.model
                and (device.model.startswith("MX") or device.model.startswith("Z3"))
            ):
                self._attr_native_value = "Multiple (VLANs)"
                self._attr_extra_state_attributes = {}
                return
            ip_value = lan_ip
        elif self._interface == "publicIp" and device:
            if device.model and device.model.startswith("MT"):
                self._attr_native_value = "N/A (Bluetooth)"
                self._attr_extra_state_attributes = {}
                return
            ip_value = device.public_ip
        else:
            uplink_data = self._get_uplink_data()
            if uplink_data:
                ip_value = uplink_data.get("ip")

        self._attr_native_value = self._truncate_value(ip_value)
        self._attr_extra_state_attributes = {
            "full_ip_address": ip_value or "Unknown"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()


class MerakiDeviceGatewaySensor(MerakiDeviceUplinkBaseSensor):
    """Sensor for Meraki device Gateway address."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        name: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_data, config_entry, interface)

        display_interface = interface.replace("Ip", "").replace("IP", "").upper()

        self.entity_description = SensorEntityDescription(
            key=f"{interface}_gateway",
            name=name or f"{display_interface} Gateway",
            icon="mdi:gateway",
        )
        self._attr_name = cast(str | None, self.entity_description.name)
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        uplink_data = self._get_uplink_data()
        gateway_value = None
        if uplink_data:
            gateway_value = uplink_data.get("gateway")

        self._attr_native_value = self._truncate_value(gateway_value)
        self._attr_extra_state_attributes = {
            "full_gateway_address": gateway_value or "Unknown"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()


class MerakiDeviceDNSSensor(MerakiDeviceUplinkBaseSensor):
    """Sensor for Meraki device DNS servers."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        name: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_data, config_entry, interface)

        display_interface = interface.replace("Ip", "").replace("IP", "").upper()

        self.entity_description = SensorEntityDescription(
            key=f"{interface}_dns",
            name=name or f"{display_interface} DNS",
            icon="mdi:dns",
        )
        self._attr_name = cast(str | None, self.entity_description.name)
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        uplink_data = self._get_uplink_data()
        dns_value = None
        if uplink_data:
            dns_servers = uplink_data.get("dns")
            if isinstance(dns_servers, list):
                dns_value = ", ".join(dns_servers)
            else:
                dns_value = dns_servers

        self._attr_native_value = cast(StateType, self._truncate_value(dns_value))
        self._attr_extra_state_attributes = {
            "full_dns_servers": dns_value or "Unknown"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()
