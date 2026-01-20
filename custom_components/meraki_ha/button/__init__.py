"""Button platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, PLATFORM_BUTTON
from .device.camera_snapshot import MerakiSnapshotButton
from .device.mt15_refresh_data import MerakiMt15RefreshDataButton
from .device.switch_port_cycle import MerakiSwitchPortCycleButton
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
    switch_port_service = entry_data.get(
        "switch_port_service"
    )  # Keeping HEAD's .get() for safety
    camera_service = entry_data["camera_service"]
    meraki_client = entry_data.get("meraki_client")
    if not meraki_client:
        _LOGGER.warning("Meraki client not available; skipping button setup.")
        return False
    button_entities: list[Entity] = []

    # switch_ports_statuses is not used with the new logic
    # switch_ports_statuses = coordinator.data.get("switch_ports_statuses", {})

    for device in coordinator.data.get("devices", []):
        # Add reboot button for all devices
        button_entities.append(
            MerakiRebootButton(device_control_service, device, config_entry)
        )

        # Add snapshot button for camera devices
        if "camera" in (device.product_type or ""):
            button_entities.append(
                MerakiSnapshotButton(coordinator, device, camera_service, config_entry)
            )

        # Add refresh data button for MT15 devices
        if (device.model or "").startswith("MT15"):
            button_entities.append(
                MerakiMt15RefreshDataButton(
                    coordinator, device, config_entry, meraki_client
                )
            )

        # Add switch port cycle buttons
        if (
            device.product_type == "switch"
            and switch_port_service
            and device.ports_statuses
        ):  # Combine conditions for safety
            for port in device.ports_statuses:
                button_entities.append(
                    MerakiSwitchPortCycleButton(
                        switch_port_service, device, port, config_entry
                    )
                )

    if button_entities:
        async_add_entities(button_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_BUTTON])
