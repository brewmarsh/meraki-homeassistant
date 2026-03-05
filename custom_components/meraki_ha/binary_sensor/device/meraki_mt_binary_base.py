"""Base class for Meraki MT binary sensor entities."""

import logging
from typing import Any, cast

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import UNDEFINED

from ...const import DOMAIN
from ...coordinators import MerakiSensorCoordinator as MerakiDataCoordinator
from ...core.models.device import MerakiDevice
from ...helpers.device_info_helpers import resolve_device_info
from ...entity import MerakiBinarySensor

_LOGGER = logging.getLogger(__name__)


class MerakiMtBinarySensor(MerakiBinarySensor):
    """Representation of a Meraki MT binary sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
        self._attr_has_entity_name = True
        if self.entity_description.name is not UNDEFINED:
            self._attr_name = cast(str | None, self.entity_description.name)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        if not self.coordinator.config_entry:
            return None
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is None:
            return
        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                self.async_write_ha_state()
                return

    def _get_metric_data(self) -> dict[str, Any] | None:
        """Return the dictionary containing data for the configured metric."""
        if self.coordinator.data is None:
            return None
        readings = self._device.readings
        if not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                metric_data = reading.get(self.entity_description.key)
                if isinstance(metric_data, dict):
                    return metric_data
        return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        metric_data = self._get_metric_data()
        if not metric_data:
            return None

        # Map metric to the key holding its value
        key_map = {
            "water": "present",
            "door": "open",
        }
        value_key = key_map.get(self.entity_description.key)

        if not value_key:
            return None

        val = metric_data.get(value_key)
        if not isinstance(val, bool):
            return None

        last_reported = metric_data.get("last_reported")
        self._attr_extra_state_attributes = {
            "last_reported": str(last_reported) if last_reported is not None else None,
        }

        return val

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        if self.coordinator.data is None:
            return False
        # The sensor is available if there is a valid dict reading for its metric.
        return self._get_metric_data() is not None
