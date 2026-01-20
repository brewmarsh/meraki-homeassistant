"""Setup helper for Meraki MT sensors."""

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
_LOGGER = logging.getLogger(__name__)


def async_setup_mt_sensors(
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
        seen = set()
        unique_descriptions = []
        for desc in sensor_descriptions:
            if desc.key not in seen:
                unique_descriptions.append(desc)
                seen.add(desc.key)
        sensor_descriptions = unique_descriptions
    for description in sensor_descriptions:
        entities.append(MerakiMtSensor(coordinator, device, description))
    return entities
