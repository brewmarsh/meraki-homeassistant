"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices, SSIDs, and clients using the Meraki SDK.
"""
import asyncio  # Required for placeholder awaitables
import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from ..meraki_api import MerakiAPIClient
# Assuming your coordinator types are defined, replace Any with them
# if possible
# from .network_coordinator import MerakiNetworkCoordinator
# from .ssid_coordinator import MerakiSsidCoordinator
from ..meraki_api.exceptions import (
    MerakiApiException,
    MerakiApiError,  # This is an alias for MerakiApiException
    MerakiApiConnectionError,
    MerakiApiAuthError, # Use this for API key errors
    MerakiApiNotFoundError, # For 404 errors
    MerakiApiRateLimitError # For 429 errors
)

_LOGGER = logging.getLogger(__name__)

# MERAKI_API_URL is no longer needed as SDK handles URLs.

# Custom exceptions like MerakiApiError, MerakiApiConnectionError, etc.,
# will be replaced by meraki.exceptions.APIError or handled directly.

class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API using the Meraki SDK.

    This class handles the communication with the Meraki API endpoints
    to retrieve various pieces of information required by the integration,
    including device tags directly within the device data.
    """

    def __init__(
        self,
        meraki_client: MerakiAPIClient,
        # network_coordinator and ssid_coordinator parameters removed
    ) -> None:
        """Initialize the MerakiApiDataFetcher.

        Args:
            meraki_client: An instance of the SDK-based MerakiAPIClient.
        """
        self.meraki_client: MerakiAPIClient = meraki_client
        # org_id can be accessed via self.meraki_client.org_id if needed
        self.org_id: str = meraki_client.org_id
        # self.network_coordinator and self.ssid_coordinator attributes removed

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # Retained for potential future use or context.
        # org_id is now available as self.org_id from the client
        # scan_interval: int, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
        # device_name_format: str, # pylint: disable=unused-argument
        # Appears unused in this method's direct logic.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        This method orchestrates calls to retrieve networks, devices (including their tags),
        SSIDs, and client information using the Meraki SDK. For MR (wireless access point)
        devices, it also fetches client count and radio settings.

        Args:
            hass: The Home Assistant instance (currently unused but common pattern).

        Returns:
            A dictionary containing lists of devices, networks, and SSIDs.
            Example: `{"devices": [...], "networks": [...], "ssids": [...]}`.
            The 'devices' list includes tags. For MR devices, it also includes
            `connected_clients_count` and `radio_settings`.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched, preventing a meaningful update.
            MerakiSDKAPIError: For underlying API communication issues from the SDK.
        """
        _LOGGER.debug("Fetching all data for organization ID: %s using SDK", self.org_id)
        # Step 1: Fetch all networks for the organization.
        networks: Optional[List[Dict[str, Any]]] = await self.async_get_networks(
            self.org_id
        )
        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki networks for org {self.org_id}.")

        # Step 2: Fetch all devices for the organization.
        devices: Optional[
            List[Dict[str, Any]]
        ] = await self.async_get_organization_devices(self.org_id)
        if devices is None:
            _LOGGER.error(
                "Could not fetch Meraki devices for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki devices for org {self.org_id}.")

        # Step 2a: Fetch additional details for MR devices (client count and radio settings)
        mr_device_tasks = []
        for device in devices:
            if device.get("model", "").upper().startswith("MR"):
                serial = device["serial"]
                mr_device_tasks.append(self._async_get_mr_device_details(device, serial))

        if mr_device_tasks:
            await asyncio.gather(*mr_device_tasks)
            # Results are directly updated in the device dictionaries within _async_get_mr_device_details

        ssids: List[Dict[str, Any]] = []
        # network_clients_data is no longer needed for device-specific client counting.
        # It might still be useful if global network client lists are needed elsewhere.
        # For now, its collection is removed to simplify based on the task.

        # Step 3: Iterate through each network to fetch its SSIDs.
        # Client fetching per network is removed as we now use get_device_clients for MRs.
        for network in networks:
            network_id: str = network["id"]
            try:
                # Fetch SSIDs for the current network
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
                ssid_data = await self.async_get_network_ssids(network_id)
                if ssid_data:  # async_get_network_ssids returns [] on 404, None on other errors
                    ssids.extend(ssid_data)
                elif ssid_data is None: # Indicates an actual error other than 404
                    _LOGGER.warning("SSID data was None for network %s, skipping SSID processing for this network.", network_id)

            except MerakiSDKAPIError as e:
                _LOGGER.warning(
                    "SDK API error during SSID data fetch for network %s: %s. Status: %s, Reason: %s. Skipping this network's SSIDs.",
                    network_id,
                    e,
                    e.status,
                    e.reason
                )
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Unexpected error fetching SSID data for network %s: %s. Skipping.",
                    network_id,
                    e,
                )

        # Step 4: Old client counting logic and restructuring is removed.
        # The 'devices' list is now directly used.

        # Step 5: Return the aggregated data
        return {
            "devices": devices, # The original devices list, now augmented with MR details
            "networks": networks,
            "ssids": ssids,
        }

    async def _async_get_mr_device_details(self, device: Dict[str, Any], serial: str) -> None:
        """Helper to fetch and store client count and radio settings for an MR device."""
        try:
            clients_data = await self.meraki_client.devices.get_device_clients(serial=serial)
            device["connected_clients_count"] = len(clients_data) if clients_data else 0
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching clients for MR device %s: %s. Setting client count to 0.",
                serial,
                e,
            )
            device["connected_clients_count"] = 0
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching clients for MR device %s: %s. Setting client count to 0.",
                serial,
                e,
            )
            device["connected_clients_count"] = 0

        try:
            radio_settings = await self.meraki_client.wireless.get_device_wireless_radio_settings(serial=serial)
            device["radio_settings"] = radio_settings
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching radio settings for MR device %s: %s. Setting radio settings to None.",
                serial,
                e,
            )
            device["radio_settings"] = None
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error fetching radio settings for MR device %s: %s. Setting radio settings to None.",
                serial,
                e,
            )
            device["radio_settings"] = None


    async def async_get_networks(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.networks.get_organization_networks(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching networks for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK."""
        _LOGGER.debug("Fetching organization devices for org ID: %s using SDK", org_id)
        try:
            return await self.meraki_client.devices.get_organization_devices(
                organization_id=org_id
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "SDK API error fetching devices for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching devices for org %s: %s. Returning None.",
                org_id,
                e,
            )
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK."""
        _LOGGER.debug("Fetching SSIDs for network ID: %s using SDK", network_id)
        try:
            return await self.meraki_client.wireless.get_network_wireless_ssids(
                network_id=network_id
            )
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.info(
                    "SSID resource not found for ntwk %s (no wireless capabilities or SSIDs via SDK), returning empty list.",
                    network_id,
                )
                return []  # Treat 404 as "no SSIDs found"
            _LOGGER.warning(
                "SDK API error fetching SSIDs for ntwk %s: %s. Returning None for this network's SSIDs.",
                network_id,
                e,
            )
            # Depending on desired behavior, could return None or empty list for other errors
            return None # Or [] if preferred to not block other network processing
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for ntwk %s: %s. Returning None.",
                network_id,
                e,
            )
            return None

    # _fetch_data method is no longer needed.
