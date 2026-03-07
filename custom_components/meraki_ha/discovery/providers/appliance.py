"""Provider for appliance port entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...binary_sensor.device.appliance_port import AppliancePortBinarySensor
from ...const.config import CONF_ENABLE_PORT_SENSORS
from ...sensor.device.appliance_port import MerakiAppliancePortSensor
from ...switch.switch_port import MerakiAppliancePortSwitch

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...core.models.device import MerakiDevice
    from ..coordinators import MerakiSwitchCoordinator

_LOGGER = logging.getLogger(__name__)


class AppliancePortProvider:
    """Provider for appliance port entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities for the appliance ports."""
        if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            return []

        entities: list[Entity] = []
        if device.appliance_ports:
            for port in device.appliance_ports:
                entities.append(MerakiAppliancePortSensor(coordinator, device, port))
                entities.append(AppliancePortBinarySensor(coordinator, device, port))
                entities.append(
                    MerakiAppliancePortSwitch(coordinator, device, port, config_entry)
                )
        return entities
