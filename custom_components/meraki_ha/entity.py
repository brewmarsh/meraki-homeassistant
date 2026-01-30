"""Base entity for all Meraki entities."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MerakiDataUpdateCoordinator


class MerakiEntity(CoordinatorEntity):
    """Base Meraki entity."""

    coordinator: MerakiDataUpdateCoordinator

    _attr_has_entity_name = True
