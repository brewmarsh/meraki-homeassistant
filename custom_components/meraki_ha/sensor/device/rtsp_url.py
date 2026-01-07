"""Sensor entity for displaying the RTSP URL of a camera."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...core.utils.network_utils import construct_rtsp_url
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiRtspUrlSensor(CoordinatorEntity, SensorEntity):
    """
    Representation of an RTSP URL sensor.

    This sensor is driven by the central MerakiDataCoordinator, which
    ensures that the state is always in sync with the latest data from the
    Meraki API.
    """

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_data = device_data
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_data['serial']}-rtsp-url"
        self._attr_name = format_entity_name(
            format_device_name(self._device_data, self._config_entry.options),
            "RTSP URL",
        )
        self._attr_icon = "mdi:cctv"

        # Set availability based on model
        model = self._device_data.get("model", "")
        if model.startswith("MV2"):
            self._attr_available = False

        # Set initial state
        self._update_state()

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_data["serial"]:
                    return dev_data
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_data = self._get_current_device_data()
        if current_data:
            self._device_data = current_data
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self._get_current_device_data() is not None

    def _update_state(self) -> None:
        """Update the sensor's state based on the latest device data."""
        # Always get fresh data from coordinator
        device_data = self._get_current_device_data() or self._device_data

        video_settings = device_data.get("video_settings", {})
        lan_ip = device_data.get("lanIp")
        if lan_ip:
            self._attr_native_value = construct_rtsp_url(lan_ip)
            return

        api_url = video_settings.get("rtspUrl")
        if api_url and api_url.startswith("rtsp://"):
            self._attr_native_value = api_url
            return

        self._attr_native_value = "Not available"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_data["serial"])},
            name=format_device_name(self._device_data, self._config_entry.options),
            model=self._device_data.get("model"),
            manufacturer="Cisco Meraki",
        )

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled by default."""
        model = self._device_data.get("model", "")
        return not model.startswith("MV2")
