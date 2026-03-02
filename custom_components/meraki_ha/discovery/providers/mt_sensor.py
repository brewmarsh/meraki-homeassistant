"""Provider for MT40 power monitoring entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...descriptions import (
    MT_CURRENT_DESCRIPTION,
    MT_ENERGY_DESCRIPTION,
    MT_FREQUENCY_DESCRIPTION,
    MT_POWER_DESCRIPTION,
    MT_POWER_FACTOR_DESCRIPTION,
    MT_VOLTAGE_DESCRIPTION,
)
from ...sensor.device.meraki_mt_base import MerakiMtSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ..coordinators import MerakiMainCoordinator
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MT40PowerMonitorProvider:
    """Provider for MT40 power monitoring entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get power monitoring entities for MT40 smart outlets."""
        descriptions = [
            MT_POWER_DESCRIPTION,
            MT_VOLTAGE_DESCRIPTION,
            MT_CURRENT_DESCRIPTION,
            MT_POWER_FACTOR_DESCRIPTION,
            MT_FREQUENCY_DESCRIPTION,
            MT_ENERGY_DESCRIPTION,
        ]
        return [MerakiMtSensor(coordinator, device, desc) for desc in descriptions]
