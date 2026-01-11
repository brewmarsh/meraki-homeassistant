"""Device handler for Meraki MT sensors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...binary_sensor.device.meraki_mt_binary_base import MerakiMtBinarySensor
from ...const import CONF_ENABLE_DEVICE_STATUS
from ...helpers.logging_helper import MerakiLoggers
from ...sensor.device.device_status import MerakiDeviceStatusSensor
from ...sensor.device.meraki_mt_base import MerakiMtSensor
from ...sensor_defs.mt_sensors import MT_BINARY_SENSOR_MODELS, MT_SENSOR_MODELS
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


_LOGGER = MerakiLoggers.DISCOVERY


class MTHandler(BaseDeviceHandler):
    """Handler for MT series sensors."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MTHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService | None,  # Unused
        control_service: DeviceControlService,
        network_control_service: NetworkControlService | None,  # Unused
    ) -> MTHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
        )

    def _get_model_prefix(self, model: str) -> str | None:
        """Extract the MT model prefix (e.g., 'MT15' from 'MT15-HW')."""
        # Check for known MT model prefixes
        for known_model in MT_SENSOR_MODELS:
            if model.upper().startswith(known_model):
                return known_model
        return None

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the device."""
        entities: list[Entity] = []
        model = self.device.get("model")
        if not model:
            return []

        # Device status sensor (common to all MT devices)
        if self._config_entry.options.get(CONF_ENABLE_DEVICE_STATUS, True):
            entities.append(
                MerakiDeviceStatusSensor(
                    self._coordinator, self.device, self._config_entry
                )
            )

        # Get the model prefix for lookup (e.g., MT15-HW -> MT15)
        model_prefix = self._get_model_prefix(model)
        if not model_prefix:
            _LOGGER.debug("Unknown MT sensor model: %s", model)
            return entities  # Return status sensor even for unknown models

        # Look up supported sensors for this model
        sensor_descriptions = MT_SENSOR_MODELS.get(model_prefix)
        if sensor_descriptions:
            for description in sensor_descriptions:
                entities.append(
                    MerakiMtSensor(self._coordinator, self.device, description)
                )

        # Look up supported binary sensors for this model
        binary_sensor_descriptions = MT_BINARY_SENSOR_MODELS.get(model_prefix, [])
        for binary_description in binary_sensor_descriptions:
            entities.append(
                MerakiMtBinarySensor(self._coordinator, self.device, binary_description)
            )

        return entities
