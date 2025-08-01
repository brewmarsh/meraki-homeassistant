"""Sensor for Meraki camera RTSP URL."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...core.coordinators.device import MerakiDeviceCoordinator
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Meraki camera RTSP URL sensors from a config entry."""
    device_coordinator = hass.data[DOMAIN][config_entry.entry_id]["device_coordinator"]
    entities = []
    for device in device_coordinator.data.get("devices", []):
        if device.get("productType") == "camera":
            entities.append(MerakiCameraRTSPUrlSensor(device_coordinator, device))
    async_add_entities(entities, True)


class MerakiCameraRTSPUrlSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki camera RTSP URL sensor."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_rtsp_url"
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{self._device['name']} RTSP URL", "camera", name_format
        )
        self._attr_icon = "mdi:video-stream"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self._device.get("video_settings", {}).get("externalRtspEnabled"):
            return self._device.get("video_settings", {}).get("rtspUrl")
        return "disabled"
