"""The Meraki Home Assistant integration.

This component provides integration with the Cisco Meraki cloud-managed
networking platform. It allows users to monitor and potentially control
aspects of their Meraki networks and devices within Home Assistant.
"""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DATA_CLIENT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    DATA_COORDINATOR,
    DATA_COORDINATORS,
)
from .core.api.client import MerakiAPIClient
from .core.coordinators.device import MerakiDeviceCoordinator
from .core.coordinators.network import MerakiNetworkCoordinator
from .webhook import async_register_webhook, async_unregister_webhook

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry.

    Args:
      hass: The Home Assistant instance
      entry: The config entry to set up

    Returns:
      True if setup was successful, False otherwise

    Raises:
      KeyError: If required configuration keys are missing
    """
    try:
        api_key: str = entry.data[CONF_MERAKI_API_KEY]
        org_id: str = entry.data[CONF_MERAKI_ORG_ID]
    except KeyError as err:
        _LOGGER.error("Missing required configuration: %s", err)
        return False

    # Get scan interval from options
    try:
        scan_interval_seconds: int = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        if scan_interval_seconds <= 0:
            raise ValueError("Scan interval must be positive")
    except (ValueError, TypeError) as err:
        _LOGGER.error(
            "Invalid scan_interval in options: %s. Using default: %s seconds.",
            err,
            DEFAULT_SCAN_INTERVAL,
        )
        scan_interval_seconds = DEFAULT_SCAN_INTERVAL

    update_interval = timedelta(seconds=scan_interval_seconds)

    # Create API client
    api_client = MerakiAPIClient(
        api_key=entry.data[CONF_MERAKI_API_KEY],
        org_id=entry.data[CONF_MERAKI_ORG_ID],
    )

    # Create the main coordinator
    device_coordinator = MerakiDeviceCoordinator(
        hass=hass,
        api_client=api_client,
        name="device_coordinator",
        update_interval=update_interval,
    )
    network_coordinator = MerakiNetworkCoordinator(
        hass=hass,
        api_client=api_client,
        name="network_coordinator",
        update_interval=update_interval,
    )

    # Store the coordinators and API client
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "device_coordinator": device_coordinator,
        "network_coordinator": network_coordinator,
        DATA_CLIENT: api_client,
    }

    # Perform initial data update
    try:
        await device_coordinator.async_config_entry_first_refresh()
        await network_coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Failed to perform initial data update: %s", err)
        return False

    # Set up the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register webhook
    if "webhook_id" not in entry.data:
        # TODO: Generate a unique webhook ID and secret
        webhook_id = "your_webhook_id"
        secret = "your_secret"
        await async_register_webhook(hass, webhook_id, secret, api_client)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "webhook_id": webhook_id, "secret": secret}
        )

    # Register update listener to handle configuration changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry.

    This function is called when Home Assistant is removing the integration setup.
    It unloads the platforms, closes the API client session, and cleans up
    data stored in `hass.data`.

    Args:
      hass: The Home Assistant instance, used to access integration data for cleanup
         and to unload platforms.
      entry: The ConfigEntry object for this integration instance, used to identify
          the data and platforms to unload.

    Returns:
      True if all unload operations are successful, False otherwise.
    """
    # Unregister webhook
    if "webhook_id" in entry.data:
        api_client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        await async_unregister_webhook(hass, entry.data["webhook_id"], api_client)

    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
            domain_entry_data = hass.data[DOMAIN].pop(entry.entry_id)
            meraki_client_instance = domain_entry_data.get(DATA_CLIENT)
            if meraki_client_instance and hasattr(meraki_client_instance, "close"):
                try:
                    await meraki_client_instance.close()
                except Exception as e:
                    _LOGGER.error(
                        "Error closing Meraki API client session for entry %s: %s",
                        entry.entry_id,
                        e,
                        exc_info=True,
                    )
            elif meraki_client_instance:
                _LOGGER.warning(
                    "Meraki API client for entry %s does not have a 'close' method.",
                    entry.entry_id,
                )
            else:
                coordinator = domain_entry_data.get("coordinator")
                if (
                    coordinator
                    and hasattr(coordinator, "meraki_client")
                    and coordinator.meraki_client
                    and hasattr(coordinator.meraki_client, "close")
                ):
                    try:
                        await coordinator.meraki_client.close()
                    except Exception as e:
                        _LOGGER.error(
                            "Error closing Meraki API client session (via legacy coordinator attribute) for entry %s: %s",
                            entry.entry_id,
                            e,
                            exc_info=True,
                        )
                else:
                    _LOGGER.warning(
                        "Meraki API client not found at expected paths for entry %s during unload. Client session may not be closed.",
                        entry.entry_id,
                    )

            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)
    else:
        _LOGGER.error("Failed to unload Meraki platforms for entry: %s", entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
