# custom_components/meraki_ha/coordinators/ssid_device_coordinator.py
"""Coordinator for Meraki SSID Devices."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import DOMAIN, DATA_CLIENT  # Added DATA_CLIENT
from ..meraki_api import MerakiAPIClient  # Added MerakiAPIClient
from .api_data_fetcher import MerakiApiDataFetcher  # To access fetched SSIDs

_LOGGER = logging.getLogger(__name__)


class SSIDDeviceCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):
    """Manages fetching and updating SSID data and registers SSIDs as devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api_data_fetcher: MerakiApiDataFetcher,
        update_interval: timedelta,
    ):
        """Initialize SSIDDeviceCoordinator."""
        self.config_entry = config_entry
        self.api_data_fetcher = api_data_fetcher
        # The unique identifier for this coordinator will be based on the config entry's unique ID
        # to ensure it's distinct per Meraki organization setup.
        coordinator_name = (
            f"{DOMAIN} SSIDs ({config_entry.unique_id or config_entry.entry_id})"
        )

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
        if (
            not self.api_data_fetcher.last_update_success
            or self.api_data_fetcher.data is None
        ):
            _LOGGER.warning(
                "Main API data fetcher has not successfully updated or has no data. Skipping SSID device update."
            )
            # If we cannot get fresh data, it's better to return the last known good data
            # or raise UpdateFailed if no data has ever been fetched.
            if (
                self.data
            ):  # If there's old data, return it to avoid entities erroring out
                return self.data
            raise UpdateFailed("Main API data fetcher has no data available for SSIDs.")

        all_ssids_from_fetcher: List[Dict[str, Any]] = self.api_data_fetcher.data.get(
            "ssids", []
        )
        _LOGGER.debug(
            f"SSIDCoordinator: Retrieved {len(all_ssids_from_fetcher)} total SSIDs from api_data_fetcher before filtering."
        )

        # --- Filter SSIDs ---
        # We are only interested in SSIDs that are currently enabled, as these are the ones
        # that will typically have associated entities (sensors, switches).
        enabled_ssids: List[Dict[str, Any]] = []
        disabled_ssids_samples: List[Dict[str, Any]] = []  # For logging
        enabled_ssids_log_samples: List[Dict[str, Any]] = []  # For logging

        for ssid_info in all_ssids_from_fetcher:
            # Create a smaller dictionary for logging purposes to keep log messages concise.
            log_sample = {
                "name": ssid_info.get("name"),
                "number": ssid_info.get("number"),
                "enabled": ssid_info.get("enabled"),
                "networkId": ssid_info.get("networkId"),
            }
            if (
                ssid_info.get("enabled") is True
            ):  # Check if the 'enabled' flag is explicitly True.
                enabled_ssids.append(ssid_info)  # Add to the list of SSIDs to process.
                if (
                    len(enabled_ssids_log_samples) < 3
                ):  # Log up to 3 samples for debugging.
                    enabled_ssids_log_samples.append(log_sample)
            else:  # SSID is not enabled.
                if (
                    len(disabled_ssids_samples) < 3
                ):  # Log up to 3 samples of disabled SSIDs.
                    disabled_ssids_samples.append(log_sample)

        _LOGGER.debug(
            f"SSIDCoordinator: Found {len(enabled_ssids)} enabled SSIDs after filtering."
        )

        if disabled_ssids_samples:
            _LOGGER.debug(
                f"SSIDCoordinator: Samples of SSIDs FILTERED OUT (e.g., disabled): {disabled_ssids_samples}"
            )
        elif all_ssids_from_fetcher:  # Only log if there were SSIDs to begin with
            _LOGGER.debug(
                "SSIDCoordinator: No SSIDs were filtered out (all were enabled or list was empty and no disabled samples)."
            )
        else:
            _LOGGER.debug("SSIDCoordinator: Initial list of SSIDs was empty.")

        if enabled_ssids_log_samples:
            _LOGGER.debug(
                f"SSIDCoordinator: Samples of SSIDs TO BE PROCESSED (enabled): {enabled_ssids_log_samples}"
            )
        elif (
            enabled_ssids
        ):  # If list has items but samples somehow not logged (shouldn't happen with this logic)
            _LOGGER.debug(
                "SSIDCoordinator: Enabled SSIDs are present but no samples logged (unexpected)."
            )
        else:  # No enabled SSIDs
            _LOGGER.debug("SSIDCoordinator: No enabled SSIDs to be processed.")

        # Performance warning for fetching client counts per SSID
        if len(enabled_ssids) > 15:  # Arbitrary threshold, adjust as needed
            _LOGGER.warning(
                f"High number of enabled SSIDs ({len(enabled_ssids)}) detected. "
                "Fetching client counts for each SSID may lead to API rate limiting "
                "or performance degradation."
            )

        if not enabled_ssids:
            _LOGGER.info(
                "SSIDCoordinator: No enabled SSIDs found after filtering. No SSID devices to update/create."
            )
            # If there were previously registered devices for SSIDs that are now disabled,
            # they will no longer be updated by this coordinator.
            # HA's device registry policy will determine if they are eventually auto-removed
            # or need explicit removal (not handled by this change).
            # For now, just return empty, so no entities are created/updated for disabled SSIDs.
            return {}

        # Retrieve the MerakiAPIClient instance
        meraki_client: MerakiAPIClient = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ][DATA_CLIENT]
        if not meraki_client:
            _LOGGER.error(
                "MerakiAPIClient not found in hass.data. Cannot fetch SSID details."
            )
            raise UpdateFailed(
                "MerakiAPIClient not available for SSID detail fetching."
            )

        detailed_ssid_data_map: Dict[str, Dict[str, Any]] = (
            {}
        )  # Stores detailed data for each enabled SSID.
        device_registry = dr.async_get(self.hass)  # Get device registry instance.

        # Cache for clients per network to avoid redundant API calls for SSIDs on the same network.
        network_clients_cache: Dict[str, List[Dict[str, Any]]] = {}

        # --- Process each enabled SSID ---
        for (
            ssid_summary_data
        ) in (
            enabled_ssids
        ):  # Iterate through the list of SSIDs that are marked as enabled.
            network_id = ssid_summary_data.get("networkId")
            ssid_number = ssid_summary_data.get(
                "number"
            )  # This is the Meraki SSID number (0-14).
            ssid_name_summary = ssid_summary_data.get(
                "name", f"SSID {ssid_number}"
            )  # Fallback name for logging.

            if not network_id or ssid_number is None:
                _LOGGER.warning(
                    f"Enabled SSID summary data missing networkId or number, cannot fetch details or process: {ssid_summary_data}"
                )
                continue  # Skip this SSID if essential identifiers are missing.

            # Create a unique identifier for this SSID to be used for the HA "device" entry.
            # This typically combines network_id and ssid_number for uniqueness.
            unique_ssid_id = f"{network_id}_{ssid_number}"

            try:
                # Fetch detailed information for this specific SSID.
                # This call gets more data than the summary list, like specific auth modes, PSK (if applicable), etc.
                _LOGGER.debug(
                    f"Fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number})"
                )
                ssid_detail_data = await meraki_client.wireless.getNetworkWirelessSsid(
                    networkId=network_id,
                    number=str(ssid_number),  # API expects SSID number as a string.
                )

                # Merge summary data (which has 'enabled' status) with detailed data.
                # Detailed data from getNetworkWirelessSsid might not include 'enabled' if called directly.
                merged_ssid_data = {**ssid_summary_data, **ssid_detail_data}
                merged_ssid_data["unique_id"] = (
                    unique_ssid_id  # Ensure unique_id is part of the data for entities.
                )

                # Attempt to get channel information. Note: SSID channel isn't directly part of SSID config.
                # It's usually derived from AP radio settings or client connection details.
                # This 'channel' key might be populated by more advanced logic in MerakiApiDataFetcher if available,
                # or it might often be None here.
                channel = ssid_detail_data.get("channel")
                merged_ssid_data["channel"] = channel if channel else None

                # --- Client Counting for this SSID ---
                # Fetch all clients for the network (if not already cached for this network_id)
                # and then filter locally for clients connected to the current SSID.
                client_count = 0  # Default to 0 clients.
                if network_id not in network_clients_cache:  # Check cache first.
                    _LOGGER.debug(
                        f"Fetching all clients for network {network_id} using `meraki_client.networks.getNetworkClients` to count for SSID {ssid_name_summary} (Num: {ssid_number})"
                    )
                    try:
                        # Fetch clients for the entire network.
                        # Timespan and perPage are used to optimize the call.
                        all_network_clients_response = await meraki_client.networks.getNetworkClients(
                            networkId=network_id,
                            timespan=900,  # Get clients seen in the last 15 minutes.
                            perPage=1000,  # Attempt to get all clients in one page if possible.
                        )
                        # Store fetched clients in cache.
                        network_clients_cache[network_id] = (
                            all_network_clients_response
                            if isinstance(all_network_clients_response, list)
                            else []
                        )
                        _LOGGER.debug(
                            f"Fetched {len(network_clients_cache[network_id])} clients for network {network_id}."
                        )
                    except AttributeError as e:  # Debugging for SDK method issues.
                        _LOGGER.error(
                            f"AttributeError when trying to fetch clients for network {network_id} using `meraki_client.networks.getNetworkClients`: {e}"
                        )
                        _LOGGER.error(
                            f"Dir of meraki_client (AsyncDashboardAPI): {dir(meraki_client)}"
                        )
                        if hasattr(meraki_client, "networks"):
                            _LOGGER.error(
                                f"Dir of meraki_client.networks (AsyncNetworks): {dir(meraki_client.networks)}"
                            )
                        else:
                            _LOGGER.error("meraki_client has no 'networks' attribute.")
                        network_clients_cache[network_id] = (
                            []
                        )  # Cache empty list on error.
                    except Exception as e:  # Catch other errors during client fetching.
                        _LOGGER.warning(
                            f"Could not fetch clients for network {network_id} using `meraki_client.networks.getNetworkClients`: {e}"
                        )
                        network_clients_cache[network_id] = (
                            []
                        )  # Cache empty list on error.

                # Filter clients from the network cache that are connected to the current SSID number.
                current_network_clients = network_clients_cache.get(
                    network_id, []
                )  # Use .get for safety.

                if current_network_clients:
                    current_ssid_clients = [
                        client
                        for client in current_network_clients # current_network_clients is already checked for None above indirectly
                        if str(client.get("ssid", "")) == str(ssid_summary_data.get("name", "")) # Compare with SSID name
                    ]
                    client_count = len(current_ssid_clients)

                else: # Should not happen if network_id was in cache and had clients, but good for safety
                    pass # No specific debug message needed here after removal of SSID_CLIENT_DEBUG


                merged_ssid_data["client_count"] = (
                    client_count  # Add client count to the SSID data.
                )
                _LOGGER.debug(
                    f"Client count for SSID {ssid_name_summary} (Num: {ssid_number}) on network {network_id}: {client_count}"
                )

                # Determine the authoritative name for the SSID device.
                authoritative_ssid_name = merged_ssid_data.get("name")
                if (
                    not authoritative_ssid_name
                ):  # Handles if name is None or empty string.
                    # Fallback if the detailed data (or summary) doesn't provide a name.
                    authoritative_ssid_name = (
                        f"SSID {merged_ssid_data.get('number', 'Unknown')}"
                    )

                # Apply device name formatting based on user's config option.
                device_name_format = self.config_entry.options.get(
                    "device_name_format", "omitted"
                )

                formatted_ssid_name = authoritative_ssid_name
                if device_name_format == "prefix":
                    formatted_ssid_name = f"[SSID] {authoritative_ssid_name}"
                elif device_name_format == "suffix":
                    formatted_ssid_name = f"{authoritative_ssid_name} [SSID]"
                # If "omitted" or other, authoritative_ssid_name is used as is.

                # --- Register SSID as an HA "Device" ---
                # This creates a logical device in Home Assistant's device registry for each SSID.
                # Entities (sensors, switches) for this SSID will then be linked to this HA device.
                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,  # Link to the integration's config entry.
                    identifiers={
                        (DOMAIN, unique_ssid_id)
                    },  # Unique identifier for this SSID "device".
                    name=formatted_ssid_name,  # User-friendly name for the SSID "device".
                    model=f"SSID (Net: {network_id}, Num: {ssid_number})",  # Model type for these logical SSID devices.
                    manufacturer="Cisco Meraki",
                    # Link this SSID "device" to its parent Network "device" in HA.
                    # This creates a hierarchy: Config Entry -> Network Device -> SSID Device -> Entities.
                    via_device=(DOMAIN, network_id),
                )
                _LOGGER.debug(
                    f"Registered/Updated device for ENABLED SSID: {formatted_ssid_name} (ID: {unique_ssid_id}, Network Parent: {network_id}). "
                    f"Format: {device_name_format}, Channel: {merged_ssid_data['channel']}, Clients: {merged_ssid_data['client_count']}. "
                    f"Full Merged Data (subset): {{name: {merged_ssid_data.get('name')}, enabled: {merged_ssid_data.get('enabled')}}}"
                )
                detailed_ssid_data_map[unique_ssid_id] = merged_ssid_data

            except Exception as e:
                _LOGGER.error(
                    f"Failed to fetch details or register device for SSID {ssid_name_summary} ({network_id}/{ssid_number}): {e}",
                    exc_info=True,
                )
                # Optionally, could use ssid_summary_data if detail fetch fails, but PSK would be missing
                # For now, if detail fetch fails, we skip this SSID for this update.
                continue

        _LOGGER.info(
            f"SSIDDeviceCoordinator processed {len(detailed_ssid_data_map)} ENABLED SSID devices with detailed data."
        )
        return detailed_ssid_data_map
