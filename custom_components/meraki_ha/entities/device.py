"""Base device entity for Meraki devices."""

from __future__ import annotations

from typing import Any, Dict

from homeassistant.helpers.device_registry import DeviceInfo

from ...const import DOMAIN
from ...coordinators import MerakiDataUpdateCoordinator
from .base import MerakiEntity


class MerakiDeviceEntity(MerakiEntity):
    """Base entity for Meraki devices."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
        name: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the device entity.

        Args:
            coordinator: The data update coordinator.
            device_data: Device data dictionary containing device information.
            name: The name of the entity.
            unique_id_suffix: Suffix to append to the device serial for a unique ID.
        """
        device_name = device_data.get(
            "name", device_data.get("serial", "Unknown Device")
        )
        device_serial = device_data.get("serial", "")
        model = device_data.get("model", "")
        firmware = device_data.get("firmware", "")

        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_serial)},
            name=device_name,
            manufacturer="Cisco Meraki",
            model=model,
            sw_version=firmware,
        )

        super().__init__(
            coordinator=coordinator,
            name=name,
            unique_id=f"{device_serial}_{unique_id_suffix}",
            device_info=device_info,
        )
        self._device_serial = device_serial

    def _get_device_data(self) -> Dict[str, Any] | None:
        """Get current device data from coordinator."""
        if not self.coordinator.data or "devices" not in self.coordinator.data:
            return None

        for device in self.coordinator.data["devices"]:
            if device.get("serial") == self._device_serial:
                return device

        return None
