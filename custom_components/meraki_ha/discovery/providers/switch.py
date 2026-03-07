"""Provider for switch port entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...binary_sensor.device.switch_port import SwitchPortSensor
from ...button.device.poe_cycle import MerakiPoECycleButton
from ...const.config import CONF_ENABLE_PORT_SENSORS
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

    from ...core.models.device import MerakiDevice
    from ..coordinators import MerakiSwitchCoordinator

_LOGGER = logging.getLogger(__name__)


class SwitchPortProvider:
    """Provider for switch port entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities for all ports on a switch."""
        if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            return []

        entities: list[Entity] = []
        if device.switch_ports:
            for port in device.switch_ports:
                # 1. Binary sensor for link status
                entities.append(SwitchPortSensor(coordinator, device, port))

                # 2. General port sensors (Power, Energy, State)
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

                # 3. Add PoE sensor only if port supports/reports power data
                if (
                    port.get("powerUsageInWh") is not None
                    or port.get("powerUsage") is not None
                ):
                    entities.append(
                        MerakiSwitchPoESensor(coordinator, device, port, config_entry)
                    )

                # 4. Control entities (Toggles and Buttons)
                entities.append(
                    MerakiSwitchPortToggle(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiPoECycleButton(coordinator, device, port, config_entry)
                )

        return entities
