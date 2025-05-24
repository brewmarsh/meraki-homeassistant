# /config/custom_components/meraki_ha/meraki_api/appliance.py
import logging
from typing import Any, Dict, List
from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiApplianceAPI:
    """Meraki appliance API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Appliance API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_device_appliance_uplinks(self, serial: str) -> Dict[str, Any]:
        """Fetch uplink settings for a Meraki MX appliance.

        Args:
            serial: Serial number of the Meraki MX appliance.

        Returns:
            A dictionary containing the uplink settings.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/appliance/uplinks/settings"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching appliance uplink settings for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching appliance uplink settings for device '{serial}': {e}"
            ) from e

    async def async_get_network_appliance_vlans(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Fetch VLANs for a Meraki network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a VLAN.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/appliance/vlans"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching VLANs for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching VLANs for network '{network_id}': {e}"
            ) from e

    async def async_get_network_appliance_vlan(
        self, network_id: str, vlan_id: str
    ) -> Dict[str, Any]:
        """Fetch a specific VLAN for a Meraki network.

        Args:
            network_id: The ID of the Meraki network.
            vlan_id: The ID of the VLAN to retrieve.

        Returns:
            A dictionary representing the specified VLAN.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/appliance/vlans/{vlan_id}"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching VLAN '{vlan_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching VLAN '{vlan_id}' for network '{network_id}': {e}"
            ) from e

    async def async_get_network_appliance_dhcp_subnet(
        self, network_id: str, subnet_id: str
    ) -> Dict[str, Any]:
        """Fetch a specific DHCP subnet for a Meraki network's appliance.

        Args:
            network_id: The ID of the Meraki network.
            subnet_id: The ID of the DHCP subnet to retrieve.

        Returns:
            A dictionary representing the specified DHCP subnet.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/appliance/dhcp/subnet/{subnet_id}"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching DHCP subnet '{subnet_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching DHCP subnet '{subnet_id}' for network '{network_id}': {e}"
            ) from e

    # Add other appliance-related API calls here as needed, following the same pattern.
    # Examples:
    # - async_get_network_appliance_security_intrusion(...)
    # - async_get_network_appliance_traffic_shaping(...)
