"""Button entity for refreshing MT15 sensor data."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.api.client import MerakiAPIClient
from ...core.utils.naming_utils import format_entity_name
from ...helpers.device_info_helpers import resolve_device_info
from ...types import MerakiDevice
=======
from ...core.api.client import MerakiAPIClient
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

_LOGGER = logging.getLogger(__name__)


class MerakiMt15RefreshDataButton(CoordinatorEntity, ButtonEntity):
    """Representation of a Meraki MT15 refresh data button."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
=======
        coordinator: MerakiDataCoordinator,
        device_info: dict[str, Any],
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
<<<<<<< HEAD
        self._device = device
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device.serial}-refresh"
        self._attr_name = f"{(device.name or 'Device')} Refresh Data"
=======
        self._device_info = device_info
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device_info['serial']}-refresh"
        self._attr_name = f"{self._device_info['name']} Refresh Data"
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
<<<<<<< HEAD
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device.serial
=======
        return resolve_device_info(self._device_info, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device_info["serial"]
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
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
        return (
<<<<<<< HEAD
            (self._device.model or "").startswith("MT15") and super().available
=======
            self._device_info.get("model", "").startswith("MT15") and super().available
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        )
