"""Sensor for Meraki WAN1 Connectivity."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
<<<<<<< HEAD
=======
from homeassistant.const import EntityCategory
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name, format_entity_name
=======
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

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
<<<<<<< HEAD
=======
    _attr_entity_category = EntityCategory.DIAGNOSTIC
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    _attr_device_class = "connectivity"  # type: ignore[assignment]

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        device_data: dict[str, Any],
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
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_wan1_connectivity"
        self._attr_name = "WAN 1 Connectivity"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Meraki",
        )
        self._update_state()

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

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_DISCONNECTED
            self._attr_extra_state_attributes = {}
            return

        wan1_ip = current_device_data.get("wan1Ip")
        device_status = str(current_device_data.get("status", "")).lower()

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
