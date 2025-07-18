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
from ..api.meraki_api import MerakiAPIClient, MerakiApiError # Added MerakiApiError
import aiohttp # Added aiohttp
from ..base_coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class SSIDDeviceCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):
    """Coordinator for Meraki SSID Devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api_data_fetcher: MerakiDataUpdateCoordinator,
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
        """Fetch and process SSID data."""
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
        for ssid_summary_data in enabled_ssids:
            network_id = ssid_summary_data.get("networkId")
            ssid_number = ssid_summary_data.get("number")
            # ssid_name_summary = ssid_summary_data.get("name", f"SSID {ssid_number}") # Only used in removed log
            unique_ssid_id = f"{network_id}_{str(ssid_number)}"

            try:
                merged_ssid_data = ssid_summary_data.copy()
                merged_ssid_data["unique_id"] = unique_ssid_id

                client_count = 0
                clients_in_current_network = [
                    client for client in all_clients_from_main_coordinator
                    if client.get("networkId") == network_id
                ]

                if clients_in_current_network:
                    current_ssid_clients = []
                    for client_idx, client_item in enumerate(clients_in_current_network):
                        if not isinstance(client_item, dict):
                            _LOGGER.warning(
                                f"Item at index {client_idx} in clients_in_current_network (Network: {network_id}) "
                                f"is not a dictionary, skipping for client count: {str(client_item)[:100]}"
                            )
                            continue
                        client_ssid_name = str(client_item.get("ssid", ""))
                        summary_ssid_name = str(ssid_summary_data.get("name", ""))
                        if client_ssid_name == summary_ssid_name:
                            current_ssid_clients.append(client_item)
                    client_count = len(current_ssid_clients)

                merged_ssid_data["client_count"] = client_count

                authoritative_ssid_name = merged_ssid_data.get("name")
                if not authoritative_ssid_name:
                    authoritative_ssid_name = f"SSID {merged_ssid_data.get('number', 'Unknown')}"

                device_name_format = self.config_entry.options.get("device_name_format", "omitted")
                formatted_ssid_name = authoritative_ssid_name
                if device_name_format == "prefix":
                    formatted_ssid_name = f"[SSID] {authoritative_ssid_name}"
                elif device_name_format == "suffix":
                    formatted_ssid_name = f"{authoritative_ssid_name} [SSID]"

                # Ensure the parent network device exists
                parent_device = device_registry.async_get_device(
                    identifiers={(DOMAIN, network_id)}
                )
                if not parent_device:
                    # Find network name for the device
                    network_name = "Unknown Network"
                    if self.api_data_fetcher.data and self.api_data_fetcher.data.get("networks"):
                        for network in self.api_data_fetcher.data["networks"]:
                            if network.get("id") == network_id:
                                network_name = network.get("name", f"Unnamed Network {network_id}")
                                break
                    device_registry.async_get_or_create(
                        config_entry_id=self.config_entry.entry_id,
                        identifiers={(DOMAIN, network_id)},
                        name=network_name,
                        manufacturer="Cisco Meraki",
                        model="Network",
                    )

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, unique_ssid_id)},
                    name=formatted_ssid_name,
                    model=f"SSID (Net: {network_id}, Num: {ssid_number})",
                    manufacturer="Cisco Meraki",
                    via_device=(DOMAIN, network_id),
                )
                detailed_ssid_data_map[unique_ssid_id] = merged_ssid_data
            except Exception as e:
                # Use ssid_summary_data for name in error log as ssid_name_summary might not be defined if first log is removed
                ssid_name_for_error = ssid_summary_data.get("name", f"SSID {ssid_summary_data.get('number', 'Unknown')}")
                _LOGGER.error(
                    f"Unexpected error during processing of SSID {ssid_name_for_error} (Network: {network_id}, Number: {ssid_number}): {e}",
                    exc_info=True,
                )
                continue

        _LOGGER.info(
            f"SSIDDeviceCoordinator successfully processed and updated {len(detailed_ssid_data_map)} ENABLED SSID devices with detailed data."
        )
        return detailed_ssid_data_map
