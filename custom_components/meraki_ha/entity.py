"""Base entity for all Meraki entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from .coordinators.base import MerakiBaseCoordinator

T = TypeVar("T", bound="MerakiBaseCoordinator")

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[T], Generic[T]):
    """Base Meraki entity."""

    _attr_has_entity_name = True

    @property
    def _serial(self) -> str | None:
        """Extract the serial number from various possible attributes."""
        if hasattr(self, "_device") and hasattr(self._device, "serial"):
            return self._device.serial
        if hasattr(self, "_device_data") and hasattr(self._device_data, "serial"):
            return self._device_data.serial
        if hasattr(self, "_device_serial"):
            return self._device_serial
        return getattr(self, "serial", None)

    @property
    def device_data(self) -> Any | None:
        """Get the updated device data robustly from ANY coordinator structure."""
        # The ultimate fallback: always return our cached device if search fails!
        fallback_device = getattr(self, "_device", None)

        if not self.coordinator.data or not self._serial:
            return fallback_device
            
        data = self.coordinator.data
        
        if isinstance(data, dict) and "devices_by_serial" in data:
            devices_map = data["devices_by_serial"]
            if isinstance(devices_map, dict) and self._serial in devices_map:
                return devices_map.get(self._serial)
                
        if isinstance(data, dict) and self._serial in data:
            return data[self._serial]
            
        if isinstance(data, list):
            for d in data:
                if getattr(d, "serial", None) == self._serial or (isinstance(d, dict) and d.get("serial") == self._serial):
                    return d
                    
        return fallback_device

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.data:
            return False

        if self._serial:
            device = self.device_data
            if device is None:
                return False

            if isinstance(device, dict):
                status = device.get("status", "offline")
            else:
                status = getattr(device, "status", "offline")

            if status is None:
                return False

            return str(status).lower() in ("online", "alerting", "dormant")

        return True

    @property
    def unique_id(self) -> str | None:
        """Return a dynamic unique ID to prevent platform collisions."""
        serial = self._serial

        if not serial and hasattr(self, "_network_id") and hasattr(self, "_ssid_number"):
            serial = f"{self._network_id}ssid{self._ssid_number}"

        if serial:
            if (
                hasattr(self, "entity_description")
                and self.entity_description
                and self.entity_description.key
            ):
                return f"{serial}_{self.entity_description.key}"

            return f"{serial}_{self.__class__.__name__.lower()}"

        return getattr(self, "_attr_unique_id", None)


class MerakiSensor(MerakiEntity[T], SensorEntity, Generic[T]):
    """Base Meraki sensor entity."""


class MerakiBinarySensor(MerakiEntity[T], BinarySensorEntity, Generic[T]):
    """Base Meraki binary sensor entity."""
