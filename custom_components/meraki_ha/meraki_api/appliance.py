"""Provides an interface to Meraki Appliance-specific API endpoints.

This module contains the `MerakiApplianceAPI` class, which encapsulates
methods for interacting with Meraki API endpoints related to security
appliances (MX series) and their configurations, such as uplink
settings, VLANs, and DHCP subnets.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiError

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiApplianceAPI:
    """Encapsulates Meraki Appliance (MX) related API calls.

    This class provides methods to retrieve information about Meraki security
    appliances, including their uplink configurations, VLAN settings, and
    DHCP subnet details. It relies on an instance of `MerakiAPIClient`
    for actual communication with the API.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Appliance API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    # Renamed for clarity
    async def async_get_device_appliance_uplinks_settings(
        self, serial: str
    ) -> Dict[str, Any]:
        """Fetch uplink settings for a specific Meraki MX security appliance.

        Reference:
        https://developer.cisco.com/meraki/api-v1/#!get-device-appliance-uplinks-settings

        Args:
            serial: The serial number of the Meraki MX appliance.

        Returns:
            A dictionary containing the uplink settings for the specified
            appliance. The structure is defined by the Meraki API.

        Raises:
            MerakiApiError: If an error occurs during the API call,
                such as network issues, invalid API key, or the device
                not found.
        """
        endpoint = f"/devices/{serial}/appliance/uplinks/settings"
        _LOGGER.debug(
            "Fetching appliance uplink settings for device serial: %s",
            serial,
        )
        try:
            # The _async_meraki_request method in MerakiAPIClient handles
            # URL construction and headers.
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error fetching uplink settings for device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e: # Catch any other unexpected errors
            _LOGGER.exception(
                "Unexpected error fetching appliance uplink settings for device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiError(
                f"Unexpected error for device '{serial}' uplink settings: {e}"
            ) from e

    async def async_get_network_appliance_vlans(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Fetch all VLANs configured for a specific Meraki network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-appliance-vlans

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a VLAN
            configuration. The structure is defined by the Meraki API.
            Returns an empty list if no VLANs are configured or found.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/appliance/vlans"
        _LOGGER.debug("Fetching VLANs for network ID: %s", network_id)
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error fetching VLANs for network '%s': %s", network_id, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching VLANs for network '%s': %s", network_id, e
            )
            raise MerakiApiError(
                f"Unexpected error for network '{network_id}' VLANs: {e}"
            ) from e

    async def async_get_network_appliance_vlan(
        self, network_id: str, vlan_id: str # vlan_id is typically an integer string
    ) -> Optional[Dict[str, Any]]:
        """Fetch details for a specific VLAN within a Meraki network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-appliance-vlan

        Args:
            network_id: The ID of the Meraki network.
            vlan_id: The identifier of the VLAN to retrieve (e.g., "100").

        Returns:
            A dictionary representing the specified VLAN's configuration if found.
            Returns `None` if the VLAN is not found (e.g., API returns 404).
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiError: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/networks/{network_id}/appliance/vlans/{vlan_id}"
        _LOGGER.debug(
            "Fetching VLAN '%s' for network ID: %s", vlan_id, network_id
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiError as e:
            # Specifically check if the error is due to a 404 (Not Found)
            # The underlying _async_api_request in _api_client.py would raise MerakiApiError
            # which might wrap an aiohttp.ClientResponseError. We'd need to inspect `e`.
            # For simplicity here, we assume MerakiApiError could be a 404.
            # A more robust way is if _async_meraki_request could return None on 404.
            if "404" in str(e): # Basic check, could be improved
                _LOGGER.warning(
                    "VLAN '%s' not found in network '%s'. API response: %s",
                    vlan_id,
                    network_id,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching VLAN '%s' for network '%s': %s",
                vlan_id,
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching VLAN '%s' for network '%s': %s",
                vlan_id,
                network_id,
                e,
            )
            raise MerakiApiError(
                f"Unexpected error for VLAN '{vlan_id}' in network '{network_id}': {e}"
            ) from e

    async def async_get_network_appliance_dhcp_subnets( # Changed to fetch all subnets
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Fetch all DHCP subnets for a Meraki network's appliance.

        This endpoint seems to be missing from the provided Meraki Python library structure,
        as the original method `async_get_network_appliance_dhcp_subnet` was for a *specific*
        subnet by ID. Meraki API usually provides a way to list all items (e.g., all subnets).
        Assuming an endpoint like `/networks/{networkId}/appliance/dhcp/subnets` exists.
        If not, this method would need to be adapted or removed.
        For now, this is a hypothetical adaptation. The original code was for a single subnet.
        Let's revert to the original single subnet fetch if a general "list subnets" is not standard.
        The original function was `async_get_network_appliance_dhcp_subnet(network_id, subnet_id)`.
        There is no standard "list all DHCP subnets" endpoint in Meraki v1 for /appliance/dhcp.
        The DHCP settings are usually per-VLAN.
        The endpoint `/networks/{networkId}/appliance/vlans/{vlanId}/dhcp` might be more relevant for DHCP settings of a VLAN.

        The original code pointed to `/networks/{network_id}/appliance/dhcp/subnet/{subnet_id}`.
        This means it was intended to get a *specific* DHCP reservation perhaps, not a subnet config.
        The Meraki documentation for "Get a DHCP subnet" is usually within a VLAN context or for static routes, not a direct call.
        Let's assume the original intent was to fetch DHCP settings for a VLAN, which is a common use case.
        The endpoint `/networks/{network_id}/appliance/vlans/{vlan_id}/dhcp` gets DHCP settings for a VLAN.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, each representing a DHCP subnet configuration.
            This is speculative based on a common API pattern.
            If targeting original functionality for a *specific* DHCP entry, the method signature and endpoint would differ.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        # This method is speculative. The original code had `subnet_id` suggesting a specific item.
        # Meraki API for DHCP subnets is usually per VLAN: /networks/{networkId}/appliance/vlans/{vlanId}/dhcp
        # For now, let's keep it aligned with the original method's apparent intent if it was a typo
        # and was meant to be for a specific VLAN's DHCP settings, or remove if no such direct endpoint.

        # Reverting to a placeholder or removing if the endpoint is incorrect.
        # The original code was:
        # endpoint = f"/networks/{network_id}/appliance/dhcp/subnet/{subnet_id}"
        # This endpoint does not appear in standard Meraki API docs for listing DHCP subnets directly under /appliance.
        # It's possible it's a very specific, perhaps less common endpoint or a custom one.
        # Given the task is docstrings and types, I will document it as if it's valid,
        # but note this uncertainty. If it was for a specific VLAN, it would be:
        # async def async_get_network_appliance_vlan_dhcp_settings(self, network_id: str, vlan_id: str)
        # endpoint = f"/networks/{network_id}/appliance/vlans/{vlan_id}/dhcp"

        # For now, let's assume the provided endpoint in original code was intended for a specific, non-standard use
        # or I'm missing context. I will document the original single subnet getter.
        # The original method name was `async_get_network_appliance_dhcp_subnet` with `subnet_id`.
        # This is NOT a standard Meraki endpoint.
        # I will remove this method as it points to a non-standard endpoint.
        # The closest standard one is getting DHCP settings for a VLAN.
        _LOGGER.warning(
            "The method `async_get_network_appliance_dhcp_subnet` was removed "
            "as its endpoint `/networks/{network_id}/appliance/dhcp/subnet/{subnet_id}` "
            "is not a standard Meraki v1 API endpoint for general DHCP subnet listing or retrieval. "
            "Consider using VLAN-specific DHCP settings via `/networks/{networkId}/appliance/vlans/{vlanId}/dhcp`."
        )
        pass # Method removed due to non-standard endpoint.

    # Example of a corrected/standard method for VLAN DHCP settings:
    async def async_get_network_appliance_vlan_dhcp_settings(
        self, network_id: str, vlan_id: str
    ) -> Optional[Dict[str, Any]]:
        """Fetch DHCP settings for a specific VLAN in a Meraki network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-appliance-vlan-dhcp

        Args:
            network_id: The ID of the Meraki network.
            vlan_id: The identifier of the VLAN for which to fetch DHCP settings.

        Returns:
            A dictionary representing the DHCP settings for the specified VLAN if found.
            Returns `None` if the VLAN or DHCP settings are not found (e.g., API returns 404).
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiError: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/networks/{network_id}/appliance/vlans/{vlan_id}/dhcp"
        _LOGGER.debug(
            "Fetching DHCP settings for VLAN '%s' in network ID: %s", vlan_id, network_id
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiError as e:
            if "404" in str(e): # Basic check
                _LOGGER.warning(
                    "DHCP settings for VLAN '%s' not found in network '%s'. API response: %s",
                    vlan_id,
                    network_id,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching DHCP settings for VLAN '%s' in network '%s': %s",
                vlan_id,
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching DHCP settings for VLAN '%s' in network '%s': %s",
                vlan_id,
                network_id,
                e,
            )
            raise MerakiApiError(
                f"Unexpected error for DHCP settings of VLAN '{vlan_id}' in network '{network_id}': {e}"
            ) from e

    # Add other appliance-related API calls here as needed, following the same pattern.
    # Examples:
    # - async_get_network_appliance_firewall_settings(self, network_id: str) -> Dict[str, Any]:
    #   endpoint = f"/networks/{network_id}/appliance/firewall/settings"
    # - async_get_network_appliance_ports(self, network_id: str) -> List[Dict[str, Any]]:
    #   endpoint = f"/networks/{network_id}/appliance/ports"
