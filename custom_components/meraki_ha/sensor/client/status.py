"""
Sensor entity for representing the status of a Meraki client.

This module defines the `MerakiClientStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (Online/Offline)
of a specific Meraki client device.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import standardize_device_name
from ...entity import MerakiSensor

_LOGGER = logging.getLogger(__name__)


class MerakiClientStatusSensor(MerakiSensor):
    """
    Representation of a Meraki Client Status sensor.

    This sensor displays the connectivity status of a Meraki client
    (e.g., "online", "offline"). It uses SensorEntityDescription
    to define its core properties. The client status is fetched from the
    coordinator's data. Additional client details are provided as state attributes.
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        client_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """
        Initialize the Meraki Client Status sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            client_data: A dictionary containing initial information about the
                Meraki client.
            config_entry: The config entry.

        """
        super().__init__(coordinator)
        self._client_mac: str = client_data["mac"]
        self._config_entry = config_entry

        # Set device info for linking to HA device registry (as a client device)
        # Note: Clients are typically not devices in HA registry unless
        # tracked specifically. Here we create a device for the client itself.
        client_name = (
            client_data.get("description") or client_data.get("ip") or self._client_mac
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._client_mac)},
            name=standardize_device_name(client_name),
            manufacturer=client_data.get("manufacturer", "Cisco Meraki"),
            model="Client",
            serial_number=self._client_mac,
        )

        if client_data.get("recentDeviceSerial"):
            self._attr_device_info["via_device"] = (
                DOMAIN,
                str(client_data["recentDeviceSerial"]),
            )

        self.entity_description = SensorEntityDescription(
            key="client_status",
            name=f"{client_name} status",
            native_unit_of_measurement=None,
            state_class=None,
            device_class=SensorDeviceClass.ENUM,
            icon="mdi:lan-connect",
        )
        self._attr_options = ["online", "offline"]

        # Override unique_id since we are not using self._device
        self._attr_unique_id = f"{self._client_mac}_client_status"

        self._update_sensor_data(client_data)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        if self.native_value == "online":
            return "mdi:lan-connect"
        return "mdi:lan-disconnect"

    def _get_current_client_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this client from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("clients"):
            for client in self.coordinator.data["clients"]:
                if client.get("mac") == self._client_mac:
                    return client
        return None

    def _update_sensor_data(self, client_data: dict[str, Any] | None = None) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_client_data = client_data or self._get_current_client_data()

        if not current_client_data:
            # If client is not found in the list, assume offline
            self._attr_native_value = "offline"
            return

        # Determine status
        status = current_client_data.get("status", "Offline")
        self._attr_native_value = status.lower()

        # Populate attributes
        self._attr_extra_state_attributes = {
            "mac_address": current_client_data.get("mac"),
            "ip_address": current_client_data.get("ip"),
            "ip6_address": current_client_data.get("ip6"),
            "description": current_client_data.get("description"),
            "user": current_client_data.get("user"),
            "vlan": current_client_data.get("vlan"),
            "switchport": current_client_data.get("switchport"),
            "ssid": current_client_data.get("ssid"),
            "usage_sent": current_client_data.get("usage", {}).get("sent"),
            "usage_recv": current_client_data.get("usage", {}).get("recv"),
            "manufacturer": current_client_data.get("manufacturer"),
            "os": current_client_data.get("os"),
            "recent_device_serial": current_client_data.get("recentDeviceSerial"),
            "recent_device_name": current_client_data.get("recentDeviceName"),
        }

        # Filter out None attributes
        self._attr_extra_state_attributes = {
            k: v for k, v in self._attr_extra_state_attributes.items() if v is not None
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()
