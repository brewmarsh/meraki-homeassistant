"""Sensor entity for displaying the RTSP URL of a camera."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...core.utils.network_utils import construct_rtsp_url
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiRtspUrlSensor(CoordinatorEntity, SensorEntity):

    """
    Representation of an RTSP URL sensor.

    This sensor is driven by the central MerakiDataUpdateCoordinator, which
    ensures that the state is always in sync with the latest data from the
    Meraki API.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the updated device data from the coordinator's payload
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_data["serial"]:
                self._device_data = device
                break
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the sensor's state based on the latest device data."""
        video_settings = self._device_data.get("video_settings", {})
        lan_ip = self._device_data.get("lanIp")
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
