"""Provides an interface to Meraki Wireless (MR series) specific API endpoints.

This module contains the `MerakiWirelessAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to MR series access points
and wireless configurations. This includes fetching radio settings, RF profiles,
client counts, SSID configurations, and device status.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiException # Use the refined base exception

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiWirelessAPI:
    """Encapsulates Meraki Wireless (MR series Access Point) related API calls.

    Provides methods to interact with Meraki wireless devices and their
    configurations, such as radio settings, RF profiles, SSIDs, and client information.
    It relies on an instance of `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Wireless API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_device_wireless_radio_settings(
        self, serial: str
    ) -> Optional[Dict[str, Any]]:
        """Return the radio settings of a device.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-wireless-radio-settings

        Args:
            serial: The serial number of the Meraki MR access point.

        Returns:
            A dictionary containing the wireless radio settings for the device if found.
            Returns `None` if the device or settings are not found (e.g., API returns 404).
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}/wireless/radio/settings"
        _LOGGER.debug(
            "Fetching wireless radio settings for device serial: %s", serial
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Wireless radio settings not found for device '%s'. API response: %s",
                    serial,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching radio settings for device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching radio settings for device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for device '{serial}' radio settings: {e}"
            ) from e

    async def async_get_network_wireless_rf_profile(
        self, network_id: str, rf_profile_id: str
    ) -> Optional[Dict[str, Any]]:
        """Return a RF profile.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-wireless-rf-profile

        Args:
            network_id: The ID of the Meraki network.
            rf_profile_id: The ID of the RF profile to retrieve.

        Returns:
            A dictionary containing the RF profile settings if found.
            Returns `None` if the RF profile is not found (e.g., API returns 404).

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/networks/{network_id}/wireless/rfProfiles/{rf_profile_id}"
        _LOGGER.debug(
            "Fetching wireless RF profile '%s' for network ID: %s",
            rf_profile_id,
            network_id,
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "RF Profile '%s' not found in network '%s'. API response: %s",
                    rf_profile_id,
                    network_id,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching RF profile '%s' for network '%s': %s",
                rf_profile_id,
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching RF profile '%s' for network '%s': %s",
                rf_profile_id,
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for RF profile '{rf_profile_id}' in network '{network_id}': {e}"
            ) from e

    async def async_get_network_client_count( # Renamed from async_get_wireless_connected_client_count
        self, network_id: str, timespan: int = 86400 # Added timespan from clients.py
    ) -> int:
        """Gets the count of clients connected to any device in a network.

        This method fetches all clients for the network within the given timespan
        and returns the total count. If filtering by specific AP MAC is needed,
        the caller should process the full client list from `MerakiClientsAPI.async_get_network_clients`.

        Args:
            network_id: The ID of the Meraki network.
            timespan: The timespan in seconds for which to retrieve clients.
                      Defaults to 86400 seconds (24 hours).

        Returns:
            The total number of clients that have connected to the network within
            the specified timespan. Returns 0 if no clients are found or an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        # This method was originally trying to count clients for a *specific* AP MAC.
        # However, it was calling the generic /networks/{networkId}/clients endpoint,
        # which lists all clients in the network, not just for one AP.
        # To get clients for a specific AP, one should use /devices/{serial}/clients.
        # This method is now revised to count all clients in the network.
        endpoint = f"/networks/{network_id}/clients"
        params = {"timespan": timespan}
        _LOGGER.debug(
            "Fetching all clients for network '%s' to count (timespan: %d)",
            network_id,
            timespan,
        )
        try:
            clients: List[Dict[str, Any]] = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint, params=params
            )
            return len(clients) if isinstance(clients, list) else 0
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching client count for network '%s': %s",
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching client count for network '%s': %s",
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error fetching client count for network '{network_id}': {e}"
            ) from e

    async def async_get_network_wireless_ssids( # Renamed from async_get_wireless_ssids
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the SSIDs in a network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-wireless-ssids

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents an SSID
            configuration for the network. Returns an empty list if no SSIDs
            are found or an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/wireless/ssids"
        _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching SSIDs for network '%s': %s", network_id, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for network '%s': %s", network_id, e
            )
            raise MerakiApiException(
                f"Unexpected error for network '{network_id}' SSIDs: {e}"
            ) from e

    # The method `async_get_network_wireless_clients` seems redundant if
    # `MerakiClientsAPI.async_get_network_clients` already provides this.
    # Wireless clients are just clients on a wireless network.
    # If there's a specific `/wireless/clients` endpoint with different data,
    # it should be used, otherwise, defer to the generic clients endpoint.
    # Meraki API docs list `/networks/{networkId}/clients` as the primary way.
    # For now, removing this potentially redundant method.
    # async def async_get_network_wireless_clients(
    #     self, network_id: str
    # ) -> List[Dict[str, Any]]: ...

    async def async_get_device_wireless_status(
        self, serial: str
    ) -> Optional[Dict[str, Any]]:
        """Return the wireless status for an MR device.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-wireless-status

        Args:
            serial: The serial number of the Meraki MR access point.

        Returns:
            A dictionary containing the wireless status information for the device if found.
            Returns `None` if the device or status is not found (e.g., API returns 404).

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}/wireless/status"
        _LOGGER.debug("Fetching wireless status for device serial: %s", serial)
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Wireless status not found for device '%s'. API response: %s",
                    serial,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching wireless status for device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching wireless status for device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for device '{serial}' wireless status: {e}"
            ) from e

    # Add other wireless-related API calls here as needed.
    # Examples:
    # - async_get_network_wireless_settings(self, network_id: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/wireless/settings
    # - async_get_network_wireless_bluetooth_settings(self, network_id: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/wireless/bluetooth/settings
    # - async_get_device_wireless_connection_stats(self, serial: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /devices/{serial}/wireless/connectionStats
    # - async_get_device_wireless_latency_stats(self, serial: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /devices/{serial}/wireless/latencyStats
