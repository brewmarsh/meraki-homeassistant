"""Switch platform for Meraki."""

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from ..const_platform import PLATFORM_SWITCH
from .setup_helpers import async_setup_switches

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        # This entry is not ready yet, we'll wait for the coordinator to be ready
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = entry_data.get("meraki_client")
    if not meraki_client:
        _LOGGER.warning("Meraki client not available; skipping switch setup.")
        return False

    from ..discovery.service import DeviceDiscoveryService

    discovery_service: DeviceDiscoveryService = entry_data["discovery_service"]

    # Add entities from discovery service
    discovery_entities = [
        entity
        for entity in discovery_service.all_entities
        if isinstance(entity, SwitchEntity)
    ]

    seen_ids = set()
    unique_discovery_entities = []
    if discovery_entities:
        for entity in discovery_entities:
            if entity.unique_id:
                if entity.unique_id not in seen_ids:
                    seen_ids.add(entity.unique_id)
                    unique_discovery_entities.append(entity)
            else:
                unique_discovery_entities.append(entity)
        async_add_entities(unique_discovery_entities)

    # Add other switches from setup helpers
    async_setup_switches(
        hass,
        config_entry,
        coordinator,
        meraki_client,
        async_add_entities,
        added_entities=seen_ids,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SWITCH])
