"""Setup helper for Meraki MT sensors."""

import logging
from typing import List

from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator
from .device.meraki_mt_base import MerakiMtSensor
from ..sensor_defs.mt_sensors import MT_SENSOR_MODELS

_LOGGER = logging.getLogger(__name__)


def async_setup_mt_sensors(
    coordinator: MerakiDataUpdateCoordinator,
    device_info: dict,
) -> List[Entity]:
    """Set up Meraki MT sensor entities for a given device."""
    entities = []
    model = device_info.get("model")

    if not model or not model.startswith("MT"):
        return []

    sensor_descriptions = MT_SENSOR_MODELS.get(model)
    if sensor_descriptions is None:
        _LOGGER.warning("Unsupported Meraki MT model: %s", model)
        # Fallback for unknown MT models - try to create all known sensor types
        # The `available` property in the base class will prevent unsupported ones from showing up.
        sensor_descriptions = [
            desc for desc_list in MT_SENSOR_MODELS.values() for desc in desc_list
        ]
        # Remove duplicates
        seen = set()
        unique_descriptions = []
        for desc in sensor_descriptions:
            if desc.key not in seen:
                unique_descriptions.append(desc)
                seen.add(desc.key)
        sensor_descriptions = unique_descriptions

    for description in sensor_descriptions:
        entities.append(MerakiMtSensor(coordinator, device_info, description))

    return entities
