# custom_components/meraki_ha/coordinators/ssid_device_coordinator.py
"""Coordinator for Meraki SSID Devices."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import DOMAIN, DATA_CLIENT
from ..meraki_api import MerakiAPIClient, MerakiApiError # Added MerakiApiError
import aiohttp # Added aiohttp
from .api_data_fetcher import MerakiApiDataFetcher # Type hint for main coordinator

_LOGGER = logging.getLogger(__name__)


class SSIDDeviceCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):
    """Manages fetching SSID data, updating corresponding HA devices, and calculating client counts.

    This coordinator retrieves information for all enabled SSIDs within a Meraki network.
    It registers each enabled SSID as a distinct HA device.
    Client counts for each SSID are determined by:
    1. Fetching all clients for the parent network of the SSID (cached per network).
    2. Filtering these network clients locally by comparing the `ssid` attribute reported
       by each client against the configured name of the current SSID.
    The resulting count is then stored within the SSID's data.
    """

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
        """Fetch SSID data, update/create HA devices, and calculate client counts.

        This method performs the following steps:
        1. Retrieves all SSIDs from `self.api_data_fetcher.data.get("ssids", [])`.
           Each item in this list (`ssid_info`) is expected to be a dictionary, ideally
           output by `MerakiDataProcessor.process_ssids()`, containing fields like:
           - 'name' (Optional[str]): SSID name.
           - 'number' (Union[int, str]): SSID number (e.g., 0-14), critical for API calls.
           - 'enabled' (bool): Whether the SSID is enabled, critical for filtering.
           - 'networkId' (str): The ID of the network this SSID belongs to, critical.
           - 'authMode' (Optional[str]), 'splashPage' (Optional[str]), etc.
        2. Filters these SSIDs to get valid, enabled ones. Validation includes
           checking for the presence and correct types of 'enabled', 'networkId',
           and 'number' fields in each `ssid_info` dictionary.
        3. For each valid, enabled SSID (`ssid_summary_data`):
            a. Fetches detailed SSID information via an API call to
               `meraki_client.wireless.getNetworkWirelessSsid()`. The raw response
               (`ssid_detail_data_raw`) is expected to be a dictionary containing
               comprehensive SSID configuration details (e.g., 'psk', 'encryptionMode').
            b. Calculates client count:
                i. Retrieves all clients for the SSID's parent network using
                   `meraki_client.networks.getNetworkClients()`. This response
                   (`all_network_clients_response`) is cached per `networkId` for
                   the duration of this update cycle and is expected to be a list
                   of client dictionaries.
                ii. Each client dictionary (`client_item`) in this list is expected to
                    have an 'ssid' (Optional[str]) field for comparison against the
                    current SSID's name.
                iii. Filters these network clients locally.
                iv. The number of matching clients is stored as `client_count`.
            c. Merges `ssid_summary_data` with the validated `ssid_detail_data` and adds
               `unique_id` (typically `f"{network_id}_{ssid_number}"`) and `client_count`.
            d. Registers or updates an HA device for the SSID using Home Assistant's
               device registry, linking it to the parent network device.
        4. Returns a dictionary where keys are `unique_ssid_id` and values are the
           `merged_ssid_data` dictionaries for each successfully processed SSID.
        """
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
        # _LOGGER.debug( # Removed: too verbose
        #     f"SSIDCoordinator: Retrieved {len(all_ssids_from_fetcher)} total SSIDs from api_data_fetcher before filtering."
        # )

        if not isinstance(all_ssids_from_fetcher, list):
            _LOGGER.error("SSID data from main fetcher is not a list (type: %s). Cannot process SSIDs.",
                          type(all_ssids_from_fetcher).__name__)
            return self.data if self.data else {} # Return last known good data or empty

        # --- Filter SSIDs ---
        # Filter the raw list of SSIDs from the main data fetcher to get only those
        # that are enabled and have the necessary identifiers (networkId, number)
        # for further processing and API calls.
        enabled_ssids: List[Dict[str, Any]] = []
        # Logging samples for disabled/enabled can be re-added if desired, removed for diff brevity.

        for i, ssid_info in enumerate(all_ssids_from_fetcher):
            # Basic validation: ensure the item is a dictionary.
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Item at index %d in all_ssids_from_fetcher is not a dictionary, skipping: %s",
                                i, str(ssid_info)[:100])
                continue

            is_enabled = ssid_info.get("enabled")
            if not isinstance(is_enabled, bool):
                _LOGGER.warning("SSID item (Name: %s, Number: %s) 'enabled' flag is not bool (type: %s, value: %s). Defaulting to False for filtering.",
                                ssid_info.get('name', 'N/A'), ssid_info.get('number', 'N/A'),
                                type(is_enabled).__name__, str(is_enabled)[:50])
                is_enabled = False

            network_id_raw = ssid_info.get("networkId")
            if not network_id_raw or not isinstance(network_id_raw, str):
                _LOGGER.warning("SSID item (Name: %s, Number: %s) has missing or invalid 'networkId' (type: %s, value: %s). Skipping.",
                                ssid_info.get('name', 'N/A'), ssid_info.get('number', 'N/A'),
                                type(network_id_raw).__name__, str(network_id_raw)[:50])
                continue

            # Validate 'number': crucial for API calls and unique ID generation.
            ssid_number_raw = ssid_info.get("number")
            if ssid_number_raw is None: # Check for None before int conversion
                _LOGGER.warning("SSID item (Name: %s, NetworkID: %s) has missing 'number'. Skipping as it's a key identifier.",
                                ssid_info.get('name', 'N/A'), network_id_raw)
                continue
            try:
                # Ensure 'number' can be interpreted as an integer, as it's used in API calls (often as string but representing an int).
                int(ssid_number_raw)
            except (ValueError, TypeError):
                _LOGGER.warning("SSID item (Name: %s, NetworkID: %s) 'number' ('%s') is not a valid integer type. Skipping as it's a key identifier.",
                                ssid_info.get('name', 'N/A'), network_id_raw,
                                str(ssid_number_raw)[:50])
                continue

            # If all checks pass and SSID is enabled, add it to the list for processing.
            if is_enabled is True:
                current_ssid_data = ssid_info.copy()  # Work with a copy
                current_ssid_data['enabled'] = True # Ensure 'enabled' is explicitly True after validation
                enabled_ssids.append(current_ssid_data)

        _LOGGER.debug(
            f"SSIDCoordinator: Found {len(enabled_ssids)} enabled and valid SSIDs after primary filtering."
        )

        # Removed excessive logging of filtered/processed SSID samples
        # if disabled_ssids_samples:
        #     _LOGGER.debug(
        #         f"SSIDCoordinator: Samples of SSIDs FILTERED OUT (e.g., disabled): {disabled_ssids_samples}"
        #     )
        # elif all_ssids_from_fetcher:  # Only log if there were SSIDs to begin with
        #     _LOGGER.debug(
        #         "SSIDCoordinator: No SSIDs were filtered out (all were enabled or list was empty and no disabled samples)."
        #     )
        # else:
        #     _LOGGER.debug("SSIDCoordinator: Initial list of SSIDs was empty.")

        # if enabled_ssids_log_samples:
        #     _LOGGER.debug(
        #         f"SSIDCoordinator: Samples of SSIDs TO BE PROCESSED (enabled): {enabled_ssids_log_samples}"
        #     )
        # elif (
        #     enabled_ssids
        # ):  # If list has items but samples somehow not logged (shouldn't happen with this logic)
        #     _LOGGER.debug(
        #         "SSIDCoordinator: Enabled SSIDs are present but no samples logged (unexpected)."
        #     )
        # else:  # No enabled SSIDs
        if not enabled_ssids: # Simplified condition
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

        # Client data will now be sourced from the main coordinator (api_data_fetcher)
        all_clients_from_main_coordinator: List[Dict[str, Any]] = []
        if self.api_data_fetcher.data and isinstance(self.api_data_fetcher.data.get("clients"), list):
            all_clients_from_main_coordinator = self.api_data_fetcher.data["clients"]
            _LOGGER.debug(f"SSIDCoordinator successfully retrieved {len(all_clients_from_main_coordinator)} clients from main coordinator.")
        else:
            _LOGGER.warning(
                "Client list not available or not a list in main coordinator data (self.api_data_fetcher.data). "
                "SSID client counts will be 0 or based on stale data if this coordinator had previous data."
            )
            # If main coordinator has no client data, this coordinator cannot calculate client counts.
            # It might return its existing self.data if available, or an empty dict.
            # For this subtask, assume it will proceed and counts will be 0 if all_clients_from_main_coordinator is empty.

        # --- Process each enabled and validated SSID ---
        # This loop iterates through each SSID that has passed the initial filtering.
        # For each SSID, it fetches detailed configuration, calculates client count,
        # and registers/updates its corresponding "device" in Home Assistant.
        for (
            ssid_summary_data
        ) in (
            enabled_ssids
        ):  # Iterate through the list of SSIDs that are marked as enabled.
            network_id = ssid_summary_data.get("networkId") # Already validated as str
            ssid_number = ssid_summary_data.get("number")  # Already validated as int-convertible
            ssid_name_summary = ssid_summary_data.get(
                "name", f"SSID {ssid_number}"
            )  # Fallback name for logging.

            # Note: network_id and ssid_number were already validated during the filtering phase.
            # A check like `if not network_id or ssid_number is None:` would be redundant here.

            # Create a unique identifier for this SSID to be used for the HA "device" entry.
            # This typically combines network_id and ssid_number for uniqueness.
            unique_ssid_id = f"{network_id}_{str(ssid_number)}" # Ensure ssid_number is string for ID

            try:
                # Step 1: Use the SSID data directly from the bulk fetch (ssid_summary_data).
                # The individual fetch per SSID is removed as the main coordinator's data
                # is now assumed to be comprehensive.
                _LOGGER.debug(
                    f"Processing SSID {ssid_name_summary} (Network: {network_id}, Number: {ssid_number}) using data from bulk fetch."
                )
                # Make a copy to allow adding new keys like 'unique_id' and 'client_count'
                # without modifying the original item in the enabled_ssids list.
                merged_ssid_data = ssid_summary_data.copy()
                merged_ssid_data["unique_id"] = unique_ssid_id # Add the HA unique_id

                # 'channel' information: If the bulk data from MerakiApiDataFetcher includes 'channel'
                # for SSIDs (e.g., derived from AP radio data or other means), it will be in ssid_summary_data.
                # If not, merged_ssid_data.get('channel') will correctly return None.
                # No specific change needed here if 'channel' is already part of ssid_summary_data as fetched.
                # For clarity, we can ensure it's explicitly accessed via merged_ssid_data if needed by other logic.
                # merged_ssid_data["channel"] = merged_ssid_data.get("channel") # This line is effectively a no-op if using .copy()

                # Step 2: Calculate client count for this SSID.
                # This involves filtering clients from the main coordinator's data
                # and then filtering them locally to find clients connected to the current SSID.
                client_count = 0  # Initialize client count to 0.

                # Filter all_clients_from_main_coordinator to get clients for the current network_id
                clients_in_current_network = [
                    client for client in all_clients_from_main_coordinator
                    if client.get("networkId") == network_id
                ]
                _LOGGER.debug(
                    f"Found {len(clients_in_current_network)} clients in network {network_id} (from main coordinator data) "
                    f"for potential matching with SSID {ssid_name_summary}."
                )

                # Filter clients_in_current_network to count only those connected to the current SSID.
                if clients_in_current_network:
                    current_ssid_clients = []
                    for client_idx, client_item in enumerate(clients_in_current_network):
                        # Validate individual client item structure.
                        if not isinstance(client_item, dict):
                            _LOGGER.warning(
                                f"Item at index {client_idx} in clients_in_current_network (Network: {network_id}) "
                                f"is not a dictionary, skipping for client count: {str(client_item)[:100]}"
                            )
                            continue

                        # Client's 'ssid' field is compared against the current SSID's configured name.
                        client_ssid_name = str(client_item.get("ssid", "")) # Default to empty string if 'ssid' key is missing.
                        summary_ssid_name = str(ssid_summary_data.get("name", "")) # Default to empty string if 'name' is None.

                        if client_ssid_name == summary_ssid_name:
                            current_ssid_clients.append(client_item)
                    client_count = len(current_ssid_clients)
                # If clients_in_current_network is empty or no clients match, client_count remains 0.

                # Add the calculated client count to the merged SSID data.
                merged_ssid_data["client_count"] = client_count
                _LOGGER.debug(
                    f"Client count for SSID {ssid_name_summary} (Number: {ssid_number}) on network {network_id}: {client_count} (derived from main coordinator data)."
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
                    # This establishes a clear hierarchy: Config Entry -> Network Device -> SSID Device -> Entities.
                    via_device=(DOMAIN, network_id), # `network_id` is the identifier of the parent network device.
                )
                _LOGGER.debug(
                    f"Registered/Updated HA device for ENABLED SSID: {formatted_ssid_name} (ID: {unique_ssid_id}, Parent Network: {network_id}). "
                    f"Name Format: {device_name_format}, Channel: {merged_ssid_data.get('channel', 'N/A')}, Clients: {merged_ssid_data['client_count']}. "
                    f"Subset of Merged Data: {{name: {merged_ssid_data.get('name')}, enabled: {merged_ssid_data.get('enabled')}}}"
                )
                # Store the fully processed data for this SSID, keyed by its unique_ssid_id.
                # This map will be the return value of _async_update_data.
                detailed_ssid_data_map[unique_ssid_id] = merged_ssid_data

            except Exception as e: # Catch-all for errors within the main processing loop for an SSID.
                _LOGGER.error(
                    f"Unexpected error during processing of SSID {ssid_name_summary} (Network: {network_id}, Number: {ssid_number}): {e}",
                    exc_info=True, # Include stack trace for unexpected errors.
                )
                # If an error occurs (e.g., detail fetch failed earlier, or device registration failed),
                # this SSID will be skipped for the current update cycle.
                # It will not be included in `detailed_ssid_data_map`.
                continue # Move to the next SSID.

        _LOGGER.info(
            f"SSIDDeviceCoordinator successfully processed and updated {len(detailed_ssid_data_map)} ENABLED SSID devices with detailed data."
        )
        return detailed_ssid_data_map
