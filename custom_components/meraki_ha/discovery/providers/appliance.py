"""Provider for appliance port entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.const.config import CONF_ENABLE_PORT_SENSORS

from ...binary_sensor.device.appliance_port import AppliancePortBinarySensor
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
        if not device.appliance_ports:
            return entities

        for port in device.appliance_ports:
            try:
                # Basic validation: ensure port has a number
                if port.number is None:
                    _LOGGER.warning(
                        "Skipping appliance port on device %s: missing port number",
                        device.serial,
                    )
                    continue

                entities.append(MerakiAppliancePortSensor(coordinator, device, port))
                entities.append(AppliancePortBinarySensor(coordinator, device, port))
                entities.append(
                    MerakiAppliancePortSwitch(coordinator, device, port, config_entry)
                )
            except Exception as err:
                _LOGGER.error(
                    "Failed to initialize appliance port %s on device %s: %s",
                    getattr(port, "number", "unknown"),
                    device.serial,
                    err,
                    exc_info=True,
                )
        return entities
