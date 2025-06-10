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
           Each item in this list is expected to be a dictionary containing at least:
           - 'name' (Optional[str])
           - 'number' (Union[int, str]): SSID number (0-14).
           - 'enabled' (bool): Whether the SSID is enabled.
           - 'networkId' (str): The ID of the network this SSID belongs to.
        2. Filters for enabled SSIDs with valid structure (correct types for above fields).
        3. For each valid, enabled SSID:
            a. Fetches detailed SSID information via an API call to `meraki_client.wireless.getNetworkWirelessSsid()`.
               The response (`ssid_detail_data_raw`) is expected to be a dictionary.
            b. Calculates client count:
                i. Retrieves all clients for the SSID's parent network using `meraki_client.networks.getNetworkClients()`.
                   This response is cached per network ID for the duration of this update cycle.
                   The client list from the API (`all_network_clients_response`) is expected to be a list of dictionaries.
                ii. Each client dictionary in the list is expected to have an 'ssid' (Optional[str]) field for comparison.
                iii. Filters these network clients locally by comparing the client's 'ssid' field
                     with the 'name' field of the current SSID being processed.
                iv. The number of matching clients is stored as `client_count`.
            c. Registers or updates an HA device for the SSID using Home Assistant's device registry.
        4. Returns a dictionary mapping unique SSID IDs (typically `f"{network_id}_{ssid_number}"`)
           to their processed data dictionary. This data includes merged summary and detail info,
           plus the calculated `client_count` and a `unique_id`.
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
        enabled_ssids: List[Dict[str, Any]] = []
        # Logging samples for disabled/enabled can be re-added if desired, removed for diff brevity.

        for i, ssid_info in enumerate(all_ssids_from_fetcher):
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

            ssid_number_raw = ssid_info.get("number")
            if ssid_number_raw is None: # Check for None before int conversion
                _LOGGER.warning("SSID item (Name: %s, NetworkID: %s) has missing 'number'. Skipping.",
                                ssid_info.get('name', 'N/A'), network_id_raw)
                continue
            try:
                # Validate if number can be an int, as used in unique_id and API calls
                int(ssid_number_raw)
            except (ValueError, TypeError):
                _LOGGER.warning("SSID item (Name: %s, NetworkID: %s) 'number' ('%s') is not a valid integer type. Skipping.",
                                ssid_info.get('name', 'N/A'), network_id_raw,
                                str(ssid_number_raw)[:50])
                continue

            if is_enabled is True:
                current_ssid_data = ssid_info.copy()
                current_ssid_data['enabled'] = True
                enabled_ssids.append(current_ssid_data)

        _LOGGER.debug(
            f"SSIDCoordinator: Found {len(enabled_ssids)} enabled and valid SSIDs after filtering."
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
            # network_id and ssid_number are now validated from ssid_summary_data
            unique_ssid_id = f"{network_id}_{str(ssid_number)}" # Ensure ssid_number is string for ID

            try:
                # Fetch detailed information for this specific SSID.
                _LOGGER.debug(
                    f"Fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number})"
                )
                try:
                    ssid_detail_data_raw = await meraki_client.wireless.getNetworkWirelessSsid(
                        networkId=network_id, # network_id is str
                        number=str(ssid_number),  # API expects SSID number as a string.
                    )
                except MerakiApiError as e:
                    _LOGGER.warning(
                        f"Meraki API error fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number}): {e}. Status: {e.status if hasattr(e, 'status') else 'N/A'}. Skipping this SSID."
                    )
                    continue
                except aiohttp.ClientError as e:
                    _LOGGER.warning(
                        f"HTTP client error fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number}): {e}. Skipping this SSID."
                    )
                    continue
                except Exception as e:
                    _LOGGER.error(
                        f"Unexpected error fetching details for SSID {ssid_name_summary} ({network_id}/{ssid_number}): {e}",
                        exc_info=True,
                    )
                    continue

                if not isinstance(ssid_detail_data_raw, dict):
                    _LOGGER.warning(f"SSID detail data for {unique_ssid_id} is not a dictionary (type: {type(ssid_detail_data_raw).__name__}). Skipping this SSID.")
                    continue
                ssid_detail_data = ssid_detail_data_raw # Now confirmed as dict

                # Merge summary data (validated dict) with detailed data (validated dict).
                # ssid_summary_data is confirmed to be a dict from the earlier loop.
                merged_ssid_data = {**ssid_summary_data, **ssid_detail_data}
                merged_ssid_data["unique_id"] = unique_ssid_id
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
                        # Store fetched clients in cache, ensuring it's a list.
                        if isinstance(all_network_clients_response, list):
                            network_clients_cache[network_id] = all_network_clients_response
                        else:
                            _LOGGER.warning("API response for getNetworkClients (Network: %s) was not a list (type: %s). Caching empty list.",
                                            network_id, type(all_network_clients_response).__name__)
                            network_clients_cache[network_id] = []

                        _LOGGER.debug(
                            f"Fetched {len(network_clients_cache[network_id])} clients for network {network_id}."
                        )
                    except AttributeError as e:
                        _LOGGER.error(
                            f"AttributeError when trying to fetch clients for network {network_id} using `meraki_client.networks.getNetworkClients`: {e}"
                        )
                        network_clients_cache[network_id] = []
                    except MerakiApiError as e: # Catch specific API errors for client fetch
                         _LOGGER.warning(
                            f"Meraki API error fetching clients for network {network_id}: {e}. Status: {e.status if hasattr(e, 'status') else 'N/A'}. Treating as no clients for this network."
                        )
                         network_clients_cache[network_id] = []
                    except aiohttp.ClientError as e: # Catch specific HTTP errors for client fetch
                        _LOGGER.warning(
                            f"HTTP client error fetching clients for network {network_id}: {e}. Treating as no clients for this network."
                        )
                        network_clients_cache[network_id] = []
                    except Exception as e:
                        _LOGGER.warning(
                            f"Could not fetch clients for network {network_id} using `meraki_client.networks.getNetworkClients`: {e}", exc_info=True
                        )
                        network_clients_cache[network_id] = []

                current_network_clients = network_clients_cache.get(network_id, []) # current_network_clients is a list

                if current_network_clients:
                    current_ssid_clients = []
                    for client_idx, client_item in enumerate(current_network_clients):
                        if not isinstance(client_item, dict):
                            _LOGGER.warning("Item at index %d in current_network_clients (Network: %s) is not a dictionary, skipping for client count: %s",
                                            client_idx, network_id, str(client_item)[:100])
                            continue

                        # Compare the SSID name reported by the client with the configured name of the current SSID.
                        client_ssid_name = str(client_item.get("ssid", ""))
                        # ssid_summary_data is confirmed a dict with 'name' potentially None
                        summary_ssid_name = str(ssid_summary_data.get("name", ""))

                        if client_ssid_name == summary_ssid_name:
                            current_ssid_clients.append(client_item)
                    client_count = len(current_ssid_clients)
                # else: # current_network_clients is empty, client_count remains 0
                #    pass


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
