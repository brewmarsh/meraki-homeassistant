"""Button entity for refreshing MT15 sensor data."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...coordinators import MerakiSensorCoordinator
from ...core.api import MerakiApiClientProtocol
from ...core.models.device import MerakiDevice
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiMt15RefreshDataButton(MerakiEntity, ButtonEntity):
    """Representation of a Meraki MT15 refresh data button."""

    def __init__(
        self,
        coordinator: MerakiSensorCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        meraki_client: MerakiApiClientProtocol,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._device = device
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device.serial}-refresh"
        self._attr_name = "Refresh data"

    @property
    def unique_id(self) -> str | None:
        """Return the unique ID."""
        return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device.serial
        _LOGGER.info("MT15 refresh data button pressed for %s", serial)
        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=str(serial), operation="refreshData"
            )
            _LOGGER.debug("Successfully triggered refresh for MT15 sensor %s", serial)
        except Exception as e:
            _LOGGER.error("Error refreshing MT15 data for %s: %s", serial, e)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if not super().available:
            return False
        return (self._device.model or "").startswith("MT15")
