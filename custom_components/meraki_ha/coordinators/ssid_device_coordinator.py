# custom_components/meraki_ha/coordinators/ssid_device_coordinator.py
"""Coordinator for Meraki SSID Devices."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import DOMAIN, DATA_CLIENT # Added DATA_CLIENT
from ..meraki_api import MerakiAPIClient # Added MerakiAPIClient
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
        _LOGGER.debug(f"SSIDCoordinator: Retrieved {len(all_ssids_from_fetcher)} total SSIDs from api_data_fetcher before filtering.")

        enabled_ssids: List[Dict[str, Any]] = []
        disabled_ssids_samples: List[Dict[str, Any]] = []
        # Shorten sample name for brevity in logs if complex objects
        enabled_ssids_log_samples: List[Dict[str, Any]] = []

        for ssid_info in all_ssids_from_fetcher:
            # Construct a smaller dict for logging samples to keep logs cleaner
            log_sample = {
                "name": ssid_info.get("name"),
                "number": ssid_info.get("number"),
                "enabled": ssid_info.get("enabled"),
                "networkId": ssid_info.get("networkId"),
            }
            if ssid_info.get("enabled") is True:
                enabled_ssids.append(ssid_info)
                if len(enabled_ssids_log_samples) < 3: # Log up to 3 samples
                    enabled_ssids_log_samples.append(log_sample)
            else:
                if len(disabled_ssids_samples) < 3: # Log up to 3 samples
                    disabled_ssids_samples.append(log_sample)

        _LOGGER.debug(f"SSIDCoordinator: Found {len(enabled_ssids)} enabled SSIDs after filtering.")

        if disabled_ssids_samples:
            _LOGGER.debug(f"SSIDCoordinator: Samples of SSIDs FILTERED OUT (e.g., disabled): {disabled_ssids_samples}")
        elif all_ssids_from_fetcher: # Only log if there were SSIDs to begin with
            _LOGGER.debug("SSIDCoordinator: No SSIDs were filtered out (all were enabled or list was empty and no disabled samples).")
        else:
            _LOGGER.debug("SSIDCoordinator: Initial list of SSIDs was empty.")


        if enabled_ssids_log_samples:
            _LOGGER.debug(f"SSIDCoordinator: Samples of SSIDs TO BE PROCESSED (enabled): {enabled_ssids_log_samples}")
        elif enabled_ssids: # If list has items but samples somehow not logged (shouldn't happen with this logic)
             _LOGGER.debug("SSIDCoordinator: Enabled SSIDs are present but no samples logged (unexpected).")
        else: # No enabled SSIDs
            _LOGGER.debug("SSIDCoordinator: No enabled SSIDs to be processed.")

        # Performance warning for fetching client counts per SSID
        if len(enabled_ssids) > 15: # Arbitrary threshold, adjust as needed
            _LOGGER.warning(
                f"High number of enabled SSIDs ({len(enabled_ssids)}) detected. "
                "Fetching client counts for each SSID may lead to API rate limiting "
                "or performance degradation."
            )

        if not enabled_ssids:
            _LOGGER.info("SSIDCoordinator: No enabled SSIDs found after filtering. No SSID devices to update/create.")
            # If there were previously registered devices for SSIDs that are now disabled,
            # they will no longer be updated by this coordinator.
            # HA's device registry policy will determine if they are eventually auto-removed
            # or need explicit removal (not handled by this change).
            # For now, just return empty, so no entities are created/updated for disabled SSIDs.
            return {}

        # Retrieve the MerakiAPIClient instance
        meraki_client: MerakiAPIClient = self.hass.data[DOMAIN][self.config_entry.entry_id][DATA_CLIENT]
        if not meraki_client:
            _LOGGER.error("MerakiAPIClient not found in hass.data. Cannot fetch SSID details.")
            raise UpdateFailed("MerakiAPIClient not available for SSID detail fetching.")

        detailed_ssid_data_map: Dict[str, Dict[str, Any]] = {}
        device_registry = dr.async_get(self.hass)

        for ssid_summary_data in enabled_ssids:
            network_id = ssid_summary_data.get("networkId")
            ssid_number = ssid_summary_data.get("number")
            # Get initial name from summary, might be updated by detail fetch
            ssid_name_summary = ssid_summary_data.get("name", f"SSID {ssid_number}")

            if not network_id or ssid_number is None:
                _LOGGER.warning(f"Enabled SSID summary data missing networkId or number, cannot fetch details or process: {ssid_summary_data}")
                continue

            unique_ssid_id = f"{DOMAIN}_{network_id}_ssid_{ssid_number}"

            try:
                _LOGGER.debug(f"Fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number})")
                # Ensure number is string for API call as per Meraki SDK expectations
                ssid_detail_data = await meraki_client.wireless.getNetworkWirelessSsid(
                    networkId=network_id,
                    number=str(ssid_number)
                )

                # Merge summary data with detail data, detail data takes precedence
                # The summary already has networkId, number, name, enabled.
                # Detail will add/override psk, visible, and other specific settings.

                # Log the raw ssid_detail_data to understand its structure for channel info
                _LOGGER.debug(f"SSID Detail Data for {ssid_name_summary} (Num: {ssid_number}): {ssid_detail_data}")

                merged_ssid_data = {**ssid_summary_data, **ssid_detail_data}
                merged_ssid_data["unique_id"] = unique_ssid_id # Ensure unique_id is preserved/added

                # Attempt to extract channel information
                # This is speculative as 'channel' is not a standard top-level field in getNetworkWirelessSsid response.
                # It might be part of 'radiusServers' (for accounting), or per-band if available (e.g. 'fiveGhzSettings', 'twoFourGhzSettings').
                # For simplicity, we'll look for a top-level 'channel' or a common nested path if known.
                # This will likely result in None for most SSIDs based on standard API.
                channel = ssid_detail_data.get("channel") # Placeholder
                # Example: if channel was per band: channel = ssid_detail_data.get("activeBand", {}).get("channel")
                merged_ssid_data["channel"] = channel if channel else None # Ensure it's None if not found or empty

                # Fetch per-SSID client count
                client_count = 0 # Default
                try:
                    _LOGGER.debug(f"Fetching client count for SSID {ssid_name_summary} (Num: {ssid_number}, Network: {network_id})")
                    # Using a timespan of 900s (15 minutes) for "current" clients
                    # Corrected SDK method name below
                    ssid_clients = await meraki_client.wireless.get_network_wireless_ssid_clients(
                        networkId=network_id,
                        number=str(ssid_number),
                        timespan=900
                    )
                    client_count = len(ssid_clients) if ssid_clients else 0
                    _LOGGER.debug(f"Client count for SSID {ssid_name_summary} (Num: {ssid_number}): {client_count}")
                except Exception as client_e: # Catch potential API errors for this specific call
                    _LOGGER.warning(f"Could not fetch client count for SSID {ssid_name_summary} (Num: {ssid_number}): {client_e}")
                merged_ssid_data["client_count"] = client_count

                authoritative_ssid_name = merged_ssid_data.get("name")
                if not authoritative_ssid_name: # Handles if name is None or empty string
                    # Fallback if the detailed data (or summary) doesn't provide a name
                    authoritative_ssid_name = f"SSID {merged_ssid_data.get('number', 'Unknown')}"

                # Apply device_name_format for SSIDs
                device_name_format = self.config_entry.options.get("device_name_format", "omitted")

                formatted_ssid_name = authoritative_ssid_name
                if device_name_format == "prefix":
                    formatted_ssid_name = f"[SSID] {authoritative_ssid_name}"
                elif device_name_format == "suffix":
                    formatted_ssid_name = f"{authoritative_ssid_name} [SSID]"
                # If "omitted" or other, use authoritative_ssid_name as is

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, unique_ssid_id)},
                    name=formatted_ssid_name, # Use the formatted name
                    model="Wireless SSID", # Model type for SSID devices
                    manufacturer="Cisco Meraki",
                    # Link to the main integration config entry device
                    via_device=(DOMAIN, self.config_entry.entry_id),
                )
                _LOGGER.debug(
                    f"Registered/Updated device for ENABLED SSID: {formatted_ssid_name} ({unique_ssid_id}). "
                    f"Format: {device_name_format}, Channel: {merged_ssid_data['channel']}, Clients: {merged_ssid_data['client_count']}. "
                    f"Full Merged Data (subset): {{name: {merged_ssid_data.get('name')}, enabled: {merged_ssid_data.get('enabled')}}}"
                )
                detailed_ssid_data_map[unique_ssid_id] = merged_ssid_data

            except Exception as e:
                _LOGGER.error(f"Failed to fetch details or register device for SSID {ssid_name_summary} ({network_id}/{ssid_number}): {e}", exc_info=True)
                # Optionally, could use ssid_summary_data if detail fetch fails, but PSK would be missing
                # For now, if detail fetch fails, we skip this SSID for this update.
                continue

        _LOGGER.info(f"SSIDDeviceCoordinator processed {len(detailed_ssid_data_map)} ENABLED SSID devices with detailed data.")
        return detailed_ssid_data_map
