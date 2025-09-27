"""The Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
    WEBHOOK_ID_FORMAT,
    CONF_MERAKI_ORG_ID,
    CONF_AUTO_RTSP,
    DEFAULT_AUTO_RTSP,
)
from .coordinator import MerakiDataUpdateCoordinator
from .webhook import async_register_webhook
from .web_api import async_setup_api
from .core.repositories.camera_repository import CameraRepository
from .services.camera_service import CameraService
from .core.repository import MerakiRepository
from .services.device_control_service import DeviceControlService
from .core.coordinators.switch_port_status_coordinator import SwitchPortStatusCoordinator


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    async_setup_api(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    coordinator = MerakiDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    repo = MerakiRepository(coordinator.api)
    device_control_service = DeviceControlService(repo)
    camera_repo = CameraRepository(coordinator.api, entry.data[CONF_MERAKI_ORG_ID])
    camera_service = CameraService(camera_repo)
    switch_port_status_coordinator = SwitchPortStatusCoordinator(
        hass, repo, coordinator, entry
    )
    await switch_port_status_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "device_control_service": device_control_service,
        "camera_service": camera_service,
        "switch_port_status_coordinator": switch_port_status_coordinator,
    }

    # Set up webhook
    webhook_id = WEBHOOK_ID_FORMAT.format(entry_id=entry.entry_id)
    hass.data[DOMAIN][entry.entry_id]["webhook_id"] = webhook_id
    if not entry.data.get("webhook_secret"):
        secret = "".join(
            __import__("random").choice(__import__("string").ascii_letters)
            for _ in range(32)
        )
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_secret": secret}
        )
    else:
        secret = entry.data["webhook_secret"]

    await async_register_webhook(
        hass, webhook_id, secret, coordinator.api, entry=entry
    )

    # Auto-enable RTSP streams if configured
    if entry.options.get(CONF_AUTO_RTSP, DEFAULT_AUTO_RTSP):
        _LOGGER.debug("Auto-RTSP is enabled, turning on streams for all cameras")
        for device in coordinator.data.get("devices", []):
            if device.get("productType", "").startswith(
                "camera"
            ) and not device.get("model", "").startswith("MV2"):
                try:
                    await camera_service.async_set_rtsp_stream_enabled(
                        device["serial"], True
                    )
                except Exception as e:
                    _LOGGER.error(
                        "Failed to auto-enable RTSP for camera %s: %s",
                        device["serial"],
                        e,
                    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)