"""Button platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, PLATFORM_BUTTON
from .device.camera_snapshot import MerakiSnapshotButton
from .device.mt15_refresh_data import MerakiMt15RefreshDataButton
from .reboot import MerakiRebootButton

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
    coordinator = entry_data["coordinator"]
    device_control_service = entry_data["device_control_service"]
    camera_service = entry_data["camera_service"]
    meraki_client = entry_data.get("meraki_client")
    if not meraki_client:
        _LOGGER.warning("Meraki client not available; skipping button setup.")
        return False
    button_entities = []

    for device in coordinator.data.get("devices", []):
        # Add reboot button for all devices
        button_entities.append(
            MerakiRebootButton(device_control_service, device, config_entry)
        )

        # Add snapshot button for camera devices
        if "camera" in device.get("productType", ""):
            button_entities.append(
                MerakiSnapshotButton(coordinator, device, camera_service, config_entry)
            )

        # Add refresh data button for MT15 devices
        if device.get("model", "").startswith("MT15"):
            button_entities.append(
                MerakiMt15RefreshDataButton(
                    coordinator, device, config_entry, meraki_client
                )
            )

    if button_entities:
        async_add_entities(button_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_BUTTON])
