"""Button platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.meraki_ha.const.config import CONF_ENABLE_PORT_SENSORS
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.platform import PLATFORM_BUTTON

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki button entities from a config entry."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        # This entry is not ready yet, we'll wait for the coordinator to be ready
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    from ..discovery.service import DeviceDiscoveryService

    discovery_service: DeviceDiscoveryService = entry_data["discovery_service"]
    enable_ports = config_entry.options.get(CONF_ENABLE_PORT_SENSORS, False)

    # Entities have already been discovered in __init__.py
    button_entities = []
    for entity in discovery_service.all_entities:
        if not isinstance(entity, ButtonEntity):
            continue

        # Filter port-related buttons
        if not enable_ports:
            # Check class name or other identifiers for port-related buttons
            class_name = entity.__class__.__name__
            if "Port" in class_name or "PoE" in class_name:
                _LOGGER.debug("Skipping port-related button %s", entity.name)
                continue

        button_entities.append(entity)

    if button_entities:
        async_add_entities(button_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_BUTTON])
