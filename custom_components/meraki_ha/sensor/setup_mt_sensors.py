"""Setup helper for Meraki MT sensors."""

<<<<<<< HEAD
import logging

from homeassistant.helpers.entity import Entity

from ..meraki_data_coordinator import MerakiDataCoordinator
from ..sensor_defs.mt_sensors import MT_SENSOR_MODELS
from .device.meraki_mt_base import MerakiMtSensor

=======
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator
from ..descriptions import MT_SENSOR_MODELS
from ..types import MerakiDevice
from .device.meraki_mt_base import MerakiMtSensor

if TYPE_CHECKING:
    from ..types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
_LOGGER = logging.getLogger(__name__)


def async_setup_mt_sensors(
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
    device_info: dict,
) -> list[Entity]:
    """Set up Meraki MT sensor entities for a given device."""
    entities: list[Entity] = []
    model = device_info.get("model")

    if not model or not model.startswith("MT"):
        return []

    sensor_descriptions = MT_SENSOR_MODELS.get(model)
    if sensor_descriptions is None:
        _LOGGER.warning("Unsupported Meraki MT model: %s", model)
        # Fallback for unknown MT models - try to create all known sensor types
        # The `available` property will prevent unsupported ones from showing up.
        sensor_descriptions = [
            desc for desc_list in MT_SENSOR_MODELS.values() for desc in desc_list
        ]
        # Remove duplicates
=======
    coordinator: MerakiDataUpdateCoordinator, device_info: MerakiDevice | dict
) -> list[Entity]:
    """Set up Meraki MT sensor entities for a given device."""
    entities: list[Entity] = []

    if isinstance(device_info, dict):
        device = MerakiDevice.from_dict(device_info)
    else:
        device = device_info

    model = device.model
    if not model or not model.startswith("MT"):
        return []
    sensor_descriptions = MT_SENSOR_MODELS.get(model)
    if sensor_descriptions is None:
        _LOGGER.warning("Unsupported Meraki MT model: %s", model)
        sensor_descriptions = [
            desc for desc_list in MT_SENSOR_MODELS.values() for desc in desc_list
        ]
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        seen = set()
        unique_descriptions = []
        for desc in sensor_descriptions:
            if desc.key not in seen:
                unique_descriptions.append(desc)
                seen.add(desc.key)
        sensor_descriptions = unique_descriptions
<<<<<<< HEAD

    for description in sensor_descriptions:
        entities.append(MerakiMtSensor(coordinator, device_info, description))

=======
    for description in sensor_descriptions:
        entities.append(MerakiMtSensor(coordinator, device, description))
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    return entities
