"""Sensor for Meraki WAN1 Connectivity."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)

STATE_CONNECTED = "Connected"
STATE_DISCONNECTED = "Disconnected"


class MerakiWAN1ConnectivitySensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of a Meraki WAN1 Connectivity Sensor."""

    _attr_icon = "mdi:wan"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = "connectivity"  # type: ignore[assignment]

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            device_data: The device data.
            config_entry: The config entry.

        """
        super().__init__(coordinator)
        assert device_data.serial
        self._device_serial: str = device_data.serial
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_wan1_connectivity"
        self._attr_name = "WAN 1 Connectivity"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.model,
            manufacturer="Meraki",
        )
        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_DISCONNECTED
            self._attr_extra_state_attributes = {}
            return

        wan1_ip = current_device_data.wan1_ip
        device_status = str(current_device_data.status or "").lower()

        if wan1_ip and device_status == "online":
            self._attr_native_value = STATE_CONNECTED
        else:
            self._attr_native_value = STATE_DISCONNECTED

        self._attr_extra_state_attributes = {
            "wan1_ip_address": wan1_ip or "N/A",
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
