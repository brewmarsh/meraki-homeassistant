"""Setup Meraki networks."""

import logging

from homeassistant.core import HomeAssistant

from .coordinators import MerakiCoordinator, async_create_meraki_network_devices
import aiohttp

_LOGGER = logging.getLogger(__name__)


async def async_setup_networks(hass: HomeAssistant, coordinator: MerakiCoordinator):
    """Set up Meraki networks."""
    _LOGGER.debug("Setting up Meraki networks.")

    api_key = coordinator.config_entry.options.get("meraki_api_key")
    org_id = coordinator.config_entry.options.get("meraki_org_id")

    try:
        async with aiohttp.ClientSession() as session:
            await async_create_meraki_network_devices(
                hass,
                api_key,
                coordinator.config_entry.entry_id,
                org_id,
                session,  # pass session
            )
    except Exception as e:
        _LOGGER.error(f"Error setting up Meraki networks: {e}")
