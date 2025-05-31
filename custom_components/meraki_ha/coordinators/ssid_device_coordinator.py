# custom_components/meraki_ha/coordinators/ssid_device_coordinator.py
"""Coordinator for Meraki SSID Devices."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import DOMAIN
from .api_data_fetcher import MerakiApiDataFetcher # To access fetched SSIDs

_LOGGER = logging.getLogger(__name__)

class SSIDDeviceCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):
    """Manages fetching and updating SSID data and registers SSIDs as devices."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, api_data_fetcher: MerakiApiDataFetcher, update_interval: timedelta):
        """Initialize SSIDDeviceCoordinator."""
        self.config_entry = config_entry
        self.api_data_fetcher = api_data_fetcher
        # The unique identifier for this coordinator will be based on the config entry's unique ID
        # to ensure it's distinct per Meraki organization setup.
        coordinator_name = f"{DOMAIN} SSIDs ({config_entry.unique_id or config_entry.entry_id})"

        super().__init__(
            hass,
            _LOGGER,
            name=coordinator_name,
            update_interval=update_interval,
            # Data type is Dict[unique_ssid_id, ssid_data_dict]
        )

    async def _async_update_data(self) -> Dict[str, Dict[str, Any]]:
        """Fetch SSID data and update/create corresponding HA devices."""
        _LOGGER.debug("SSIDDeviceCoordinator starting _async_update_data")

        # Ensure the main data fetcher has run and has data
        if not self.api_data_fetcher.last_update_success or self.api_data_fetcher.data is None:
            _LOGGER.warning("Main API data fetcher has not successfully updated or has no data. Skipping SSID device update.")
            # If we cannot get fresh data, it's better to return the last known good data
            # or raise UpdateFailed if no data has ever been fetched.
            if self.data: # If there's old data, return it to avoid entities erroring out
                return self.data
            raise UpdateFailed("Main API data fetcher has no data available for SSIDs.")

        all_ssids_from_fetcher: List[Dict[str, Any]] = self.api_data_fetcher.data.get("ssids", [])

        _LOGGER.debug(f"Retrieved {len(all_ssids_from_fetcher)} total SSIDs from api_data_fetcher before filtering.")

        enabled_ssids = [
            ssid_info for ssid_info in all_ssids_from_fetcher if ssid_info.get("enabled") is True
        ]

        _LOGGER.debug(f"Found {len(enabled_ssids)} enabled SSIDs after filtering.")

        if not enabled_ssids:
            _LOGGER.info("No enabled SSIDs found. No SSID devices to update/create.")
            # If there were previously registered devices for SSIDs that are now disabled,
            # they will no longer be updated by this coordinator.
            # HA's device registry policy will determine if they are eventually auto-removed
            # or need explicit removal (not handled by this change).
            # For now, just return empty, so no entities are created/updated for disabled SSIDs.
            return {}

        device_registry = dr.async_get(self.hass)
        processed_ssid_devices: Dict[str, Dict[str, Any]] = {}

        for ssid_data in enabled_ssids: # Changed to iterate over filtered list
            network_id = ssid_data.get("networkId")
            ssid_number = ssid_data.get("number")
            ssid_name = ssid_data.get("name", f"SSID {ssid_number}")

            if not network_id or ssid_number is None: # ssid_number can be 0
                _LOGGER.warning(f"Enabled SSID data missing networkId or number, cannot process: {ssid_data}")
                continue

            # Create a unique and stable identifier for the SSID device
            unique_ssid_id = f"{DOMAIN}_{network_id}_ssid_{ssid_number}"

            # Add the unique_id to the ssid_data itself for easy access by entities
            ssid_data["unique_id"] = unique_ssid_id

            # Register the SSID as a device in Home Assistant
            # TODO: Determine the correct via_device identifier.
            # If network devices are registered, use (DOMAIN, network_id).
            # Otherwise, use the config entry: (DOMAIN, self.config_entry.entry_id)
            # For now, using config entry.
            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, unique_ssid_id)},
                name=f"{ssid_name} (SSID)", # Distinguish from physical APs
                model="Wireless SSID",
                manufacturer="Cisco Meraki",
                # sw_version= # Not directly applicable to an SSID itself. Could use network firmware if available.
                via_device=(DOMAIN, self.config_entry.entry_id), # Link to the integration instance
            )
            _LOGGER.debug(f"Registered/Updated device for ENABLED SSID: {ssid_name} ({unique_ssid_id})")

            processed_ssid_devices[unique_ssid_id] = ssid_data

        _LOGGER.info(f"SSIDDeviceCoordinator processed {len(processed_ssid_devices)} ENABLED SSID devices.")
        return processed_ssid_devices
