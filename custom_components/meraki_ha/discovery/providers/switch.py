"""Switch Port Provider."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...binary_sensor.device.switch_port import SwitchPortSensor
from ...button.device.poe_cycle import MerakiPoECycleButton
from ...const_conf import CONF_ENABLE_PORT_SENSORS
from ...sensor.device.switch_poe import MerakiSwitchPoESensor
from ...sensor.device.switch_port import (
    MerakiSwitchPortEnergySensor,
    MerakiSwitchPortPowerSensor,
    MerakiSwitchPortSensor,
)
from ...switch.switch_port import MerakiSwitchPortToggle

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...coordinator import MerakiDataUpdateCoordinator
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class SwitchPortProvider:
    """Provider for switch port entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            return []
        entities: list[Entity] = []
        if device.ports_statuses:
            for port in device.ports_statuses:
                entities.append(SwitchPortSensor(coordinator, device, port))
                entities.append(
                    MerakiSwitchPortSensor(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiSwitchPortEnergySensor(
                        coordinator, device, port, config_entry
                    )
                )
                if (
                    port.get("powerUsageInWh") is not None
                    or port.get("powerUsage") is not None
                ):
                    entities.append(
                        MerakiSwitchPoESensor(coordinator, device, port, config_entry)
                    )
                # RESOLVED: Updated constructor to include config_entry per beta branch
                entities.append(
                    MerakiSwitchPortToggle(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiPoECycleButton(coordinator, device, port, config_entry)
                )
        return entities
