"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .meraki_api.appliance import get_meraki_device_appliance_uplinks
from .meraki_api.exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiUplinkStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki MX Appliance Uplink Status sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")
        self._attr_name = f"{device['name']} Uplink Status"
        self._attr_unique_id = f"{device['serial']}_uplink_status"
        self._attr_icon = "mdi:upload-network-outline"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get("serial")
        _LOGGER.debug(f"Meraki: Uplink Sensor Initialized: {self._attr_name}")

    async def async_update(self) -> None:
        """Update the sensor state."""
        _LOGGER.debug(f"Meraki: Updating sensor state for {self._attr_name}")
        try:
            uplinks = await get_meraki_device_appliance_uplinks(
                self.coordinator.api_key,
                self.coordinator.org_id,
                self._device["serial"],
            )
            if uplinks and uplinks.get("uplinks"):
                self._attr_native_value = uplinks["uplinks"][0].get("status", "Unknown")
                self._attr_extra_state_attributes.update(
                    {"uplinks": uplinks.get("uplinks")}
                )
            else:
                self._attr_native_value = "Unavailable"
                self._attr_extra_state_attributes.update({"uplinks": None})
        except MerakiApiError as e:
            _LOGGER.error(f"Meraki: Error fetching uplink status: {e}")
            self._attr_native_value = "Error"
        except Exception as e:
            _LOGGER.error(f"Meraki: Unexpected error fetching uplink status: {e}")
            self._attr_native_value = "Error"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()
