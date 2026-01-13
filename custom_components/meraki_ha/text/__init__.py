"""Text platform for Meraki."""

<<<<<<< HEAD
<<<<<<< HEAD
import logging

=======
<<<<<<< HEAD
import logging

=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import asyncio
import logging

from homeassistant.components.text import TextEntity
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
<<<<<<< HEAD
from ..const import DOMAIN, PLATFORM_TEXT
from .meraki_ssid_name import MerakiSSIDNameText
=======
<<<<<<< HEAD
from ..const import DOMAIN, PLATFORM_TEXT
from .meraki_ssid_name import MerakiSSIDNameText
=======
from ..const import DOMAIN
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from ..const import DOMAIN
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
<<<<<<< HEAD
<<<<<<< HEAD
    if config_entry.entry_id not in hass.data[DOMAIN]:
=======
<<<<<<< HEAD
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = coordinator.api

    if coordinator.data:
        text_entities = [
            MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid)
            for ssid in coordinator.data.get("ssids", [])
        ]

        if text_entities:
            async_add_entities(text_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_TEXT])
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    entry_data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {})
    if not entry_data:
        _LOGGER.warning("Meraki entry data not found for %s", config_entry.entry_id)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = coordinator.api

    if coordinator.data:
        text_entities = [
            MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid)
            for ssid in coordinator.data.get("ssids", [])
        ]

        if text_entities:
            async_add_entities(text_entities)

    return True
<<<<<<< HEAD
<<<<<<< HEAD


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_TEXT])
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
