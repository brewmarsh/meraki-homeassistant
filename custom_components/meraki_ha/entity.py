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
        for attr in ("_device", "_device_data"):
            if hasattr(self, attr):
                val = getattr(self, attr)
                if isinstance(val, dict) and "serial" in val:
                    return val.get("serial")
                if hasattr(val, "serial"):
                    return val.serial

        if hasattr(self, "_device_serial"):
            return self._device_serial

        return getattr(self, "serial", None)

    @property
    def device_data(self) -> Any | None:
        """Get the updated device data robustly from ANY coordinator structure."""
        # First, try to use the coordinator's built-in get_device method
        if hasattr(self.coordinator, "get_device") and self._serial:
            device = self.coordinator.get_device(self._serial)
            if device:
                return device

        # The ultimate fallback: always return our cached device if search fails!
        fallback_device = getattr(self, "_device", None)
        if fallback_device is None:
            fallback_device = getattr(self, "_device_data", None)

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
                if getattr(d, "serial", None) == self._serial or (
                    isinstance(d, dict) and d.get("serial") == self._serial
                ):
                    return d

        return fallback_device

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.data:
            _LOGGER.warning("[%s] Unavailable: coordinator.data is empty", self.name)
            return False

        if self._serial:
            device = self.device_data
            if device is None:
                _LOGGER.warning(
                    "[%s] Unavailable: device_data is None for serial %s",
                    self.name,
                    self._serial,
                )
                return False

            # Defensively check status
            if isinstance(device, dict):
                status = device.get("status")
            else:
                status = getattr(device, "status", None)

            # FIX: If the coordinator data doesn't include a status field at all,
            # we assume it's available since the data fetch itself succeeded.
            if status is None:
                return True

            # If status is present, ensure it's not explicitly offline
            is_online = str(status).lower() in ("online", "alerting", "dormant")
            if not is_online:
                _LOGGER.warning(
                    "[%s] Unavailable: status '%s' is explicitly offline",
                    self.name,
                    status,
                )
            return is_online

        return True

    @property
    def unique_id(self) -> str | None:
        """Return a dynamic unique ID to prevent platform collisions."""
        serial = self._serial

        if (
            not serial
            and hasattr(self, "_network_id")
            and hasattr(self, "_ssid_number")
        ):
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
