"""Meraki HA event platform."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from .device.camera_motion import MerakiCameraMotionEvent

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki event entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: MerakiDataUpdateCoordinator = data["coordinator"]
    camera_service = data["camera_service"]

    if not coordinator.data or "devices" not in coordinator.data:
        _LOGGER.warning("Meraki client not available; skipping event setup.")
        return

    entities = []

    for device in coordinator.data["devices"]:
        if device.product_type == "camera":
            entities.append(
                MerakiCameraMotionEvent(coordinator, device, camera_service, entry)
            )

    async_add_entities(entities)
