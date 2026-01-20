"""Sensor entity for displaying the RTSP URL of a camera."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...core.utils.network_utils import construct_rtsp_url

_LOGGER = logging.getLogger(__name__)


class MerakiRtspUrlSensor(CoordinatorEntity, SensorEntity):
    """
    Representation of an RTSP URL sensor.

    This sensor is driven by the central MerakiDataUpdateCoordinator, which
    ensures that the state is always in sync with the latest data from the
    Meraki API.
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: dict[str, Any] | Any,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_data = device_data
        self._config_entry = config_entry
        serial = (
            device_data.serial
            if hasattr(device_data, "serial")
            else device_data["serial"]
        )
        self._attr_unique_id = f"{serial}-rtsp-url"
        device_name = format_device_name(self._device_data, self._config_entry.options)
        self._attr_name = f"[Camera] {device_name} RTSP URL"
        self._attr_icon = "mdi:cctv"

        # Set availability based on model
        model = (
            device_data.model
            if hasattr(device_data, "model")
            else device_data.get("model", "")
        )
        if model.startswith("MV2"):
            self._attr_available = False

        # Set initial state
        self._update_state()

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the updated device data from the coordinator's payload
        current_serial = (
            self._device_data.serial
            if hasattr(self._device_data, "serial")
            else self._device_data["serial"]
        )
        # coordinator.data["devices"] is a list of MerakiDevice dataclasses
        if self.coordinator.data:
            devices = self.coordinator.data.get("devices", [])
            for device in devices:
                # device is MerakiDevice
                if device.serial == current_serial:
                    self._device_data = device
                    break
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the sensor's state based on the latest device data."""
        video_settings = (
            self._device_data.video_settings
            if hasattr(self._device_data, "video_settings")
            else self._device_data.get("video_settings", {})
        ) or {}
        lan_ip = (
            self._device_data.lan_ip
            if hasattr(self._device_data, "lan_ip")
            else self._device_data.get("lanIp")
        )
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
        serial = (
            self._device_data.serial
            if hasattr(self._device_data, "serial")
            else self._device_data["serial"]
        )
        model = (
            self._device_data.model
            if hasattr(self._device_data, "model")
            else self._device_data.get("model")
        )
        return DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name=format_device_name(self._device_data, self._config_entry.options),
            model=model,
            manufacturer="Cisco Meraki",
        )

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled by default."""
        model = (
            self._device_data.model
            if hasattr(self._device_data, "model")
            else self._device_data.get("model", "")
        )
        return not model.startswith("MV2")
