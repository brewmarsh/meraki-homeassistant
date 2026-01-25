"""Base entity for all Meraki entities."""
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class MerakiEntity(CoordinatorEntity):
    """Base Meraki entity."""

    _attr_has_entity_name = True
