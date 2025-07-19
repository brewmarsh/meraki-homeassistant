"""Coordinator for Meraki device data."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.exceptions import UpdateFailed

from .base import BaseMerakiCoordinator
from ..utils import map_meraki_model_to_device_type

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(BaseMerakiCoordinator):
    """Coordinator to handle Meraki device data."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the device coordinator."""
        super().__init__(*args, **kwargs)
        self._devices: List[Dict[str, Any]] = []

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch device data from Meraki.

        Fetches all devices and enhances their data with product type mapping
        and additional device-specific information like client counts for wireless
        devices.

        Returns:
            Dict containing device data

        Raises:
            UpdateFailed: If update fails
        """
        try:
            devices = await self.api_client.get_devices(self.api_client.org_id)
            processed_devices = []

            for device in devices:
                # Skip devices without required attributes
                if not all(key in device for key in ["serial", "model"]):
                    _LOGGER.warning("Device missing required attributes: %s", device)
                    continue

                # Add product type based on model
                model = device.get("model", "")
                device["productType"] = map_meraki_model_to_device_type(model)

                # Fetch additional data for wireless devices
                if device["productType"] == "wireless":
                    try:
                        # These would be actual API calls in your implementation
                        device["connected_clients_count"] = 0  # Placeholder
                        device["radio_settings"] = {
                            "status": "unknown",
                            "24": {"channel": 0, "power": 0},
                            "5": {"channel": 0, "power": 0},
                        }
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching wireless data for device %s: %s",
                            device.get("serial"),
                            err,
                        )

                processed_devices.append(device)

            self._devices = processed_devices
            return {"devices": processed_devices}

        except Exception as err:
            _LOGGER.error("Error fetching device data: %s", err)
            raise UpdateFailed(f"Error fetching device data: {err}")

    def get_device_by_serial(self, serial: str) -> Optional[Dict[str, Any]]:
        """Get a device by its serial number.

        Args:
            serial: Device serial number

        Returns:
            Device data dictionary or None if not found
        """
        for device in self._devices:
            if device.get("serial") == serial:
                return device
        return None
