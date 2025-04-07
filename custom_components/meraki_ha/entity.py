"""Entity for meraki_ha."""

import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity):
    """Base class for Meraki entities."""

    def __init__(self, coordinator, device, ssid=None):
        """Initialize the Meraki entity."""
        super().__init__(coordinator)
        self._device = device
        self._ssid = ssid
        self._device_name = device.get("name")
        self._device_serial = device.get("serial")
        self._device_model = device.get("model")
        self._device_firmware = device.get("firmware")
        self._ssid_name = ssid.get("name") if ssid else None
        self._ssid_number = ssid.get("number") if ssid else None
        self._device_index = self._find_device_index(
            coordinator.data["devices"], self._device_serial
        )
        self._ssid_index = (
            self._find_ssid_index(
                coordinator.data["devices"][self._device_index]["ssids"],
                self._ssid_number,
            )
            if ssid
            else None
        )

    def _find_device_index(self, devices, serial):
        """Find the index of the device in the coordinator data."""
        for index, device in enumerate(devices):
            if device.get("serial") == serial:
                return index
        return None

    def _find_ssid_index(self, ssids, number):
        """Find the index of the SSID in the coordinator data."""
        for index, ssid in enumerate(ssids):
            if ssid.get("number") == number:
                return index
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=self._device_name,
            manufacturer="Cisco Meraki",
            model=self._device_model,
            sw_version=self._device_firmware,
        )
