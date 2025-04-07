"""Switch platform for meraki_ha."""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity

from .ssid_switch import MerakiSSIDSwitch, match_device_to_ssid
from ..const import DOMAIN, DATA_COORDINATOR, ATTR_SSIDS
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Meraki SSID switches."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    switches: List[SwitchEntity] = []

    relaxed_matching = coordinator.relaxed_tag_match

    for device in coordinator.data.get("devices", []):
        if device.get(ATTR_SSIDS):
            for ssid in device[ATTR_SSIDS]:
                if match_device_to_ssid(
                    ssid, coordinator.data.get("devices", []), relaxed_matching
                ):
                    switches.append(MerakiSSIDSwitch(coordinator, device, ssid))

    async_add_entities(switches)
