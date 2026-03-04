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

    seen_ids: set[str] = set()
    entities_to_add: list[SwitchEntity] = []

    def async_add_unique_entities(new_entities: list[SwitchEntity]) -> None:
        """Filter and add unique entities."""
        for entity in new_entities:
            if entity.unique_id:
                if entity.unique_id not in seen_ids:
                    seen_ids.add(entity.unique_id)
                    entities_to_add.append(entity)
                else:
                    _LOGGER.debug("Ignoring duplicate entity with ID %s", entity.unique_id)
            else:
                entities_to_add.append(entity)

    # Process discovery entities
    if discovery_entities:
        async_add_unique_entities(discovery_entities)

    # Add other switches from setup helpers using the same deduplication logic
    async_setup_switches(
        hass,
        config_entry,
        coordinator,
        meraki_client,
        async_add_unique_entities,
        added_entities=seen_ids,
    )

    if entities_to_add:
        async_add_entities(entities_to_add)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SWITCH])
