"""Sensor for Meraki WAN2 Connectivity."""

from __future__ import annotations

import logging
<<<<<<< HEAD
from typing import Any
=======
from typing import TYPE_CHECKING, Any
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)

STATE_CONNECTED = "Connected"
STATE_DISCONNECTED = "Disconnected"


class MerakiWAN2ConnectivitySensor(
    CoordinatorEntity,
    SensorEntity,
):
    """Representation of a Meraki WAN2 Connectivity Sensor."""

    _attr_icon = "mdi:wan"
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = "connectivity"  # type: ignore[assignment]

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
        self._device_serial: str = device_data["serial"]
=======
        self._device_serial: str = device_data.serial
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_wan2_connectivity"
        self._attr_name = "WAN 2 Connectivity"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
<<<<<<< HEAD
            model=device_data.get("model"),
=======
            model=device_data.model,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            manufacturer="Meraki",
        )
        self._update_state()

<<<<<<< HEAD
    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            return next(
                (
                    device
                    for device in self.coordinator.data["devices"]
                    if device.get("serial") == self._device_serial
                ),
                None,
            )
        return None
=======
    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_DISCONNECTED
            self._attr_extra_state_attributes = {}
            return

<<<<<<< HEAD
        wan2_ip = current_device_data.get("wan2Ip")
        device_status = str(current_device_data.get("status", "")).lower()
=======
        wan2_ip = current_device_data.wan2_ip
        device_status = str(current_device_data.status or "").lower()
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        if wan2_ip and device_status == "online":
            self._attr_native_value = STATE_CONNECTED
        else:
            self._attr_native_value = STATE_DISCONNECTED

        self._attr_extra_state_attributes = {
            "wan2_ip_address": wan2_ip or "N/A",
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
