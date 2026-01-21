"""Button entity for refreshing MT15 sensor data."""

from __future__ import annotations

import logging
<<<<<<< HEAD
from typing import Any
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...core.api.client import MerakiAPIClient
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.api.client import MerakiAPIClient
from ...helpers.device_info_helpers import resolve_device_info
from ...types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


class MerakiMt15RefreshDataButton(CoordinatorEntity, ButtonEntity):
    """Representation of a Meraki MT15 refresh data button."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device_info: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
<<<<<<< HEAD
        self._device_info = device_info
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device_info['serial']}-refresh"
        self._attr_name = f"{self._device_info['name']} Refresh Data"
=======
        self._device = device
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device.serial}-refresh"
        self._attr_name = f"{(device.name or 'Device')} Refresh Data"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
<<<<<<< HEAD
        return resolve_device_info(self._device_info, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device_info["serial"]
=======
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device.serial
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        _LOGGER.info("MT15 refresh data button pressed for %s", serial)
        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=serial, operation="refreshData"
            )
            _LOGGER.debug("Successfully triggered refresh for MT15 sensor %s", serial)
        except Exception as e:
            _LOGGER.error("Error refreshing MT15 data for %s: %s", serial, e)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
<<<<<<< HEAD
        return (
            self._device_info.get("model", "").startswith("MT15") and super().available
        )
=======
        return (self._device.model or "").startswith("MT15") and super().available
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
