# /config/custom_components/meraki_ha/meraki_api/switch.py
import logging
from typing import Any, Dict, List
from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchAPI:
    """Meraki switch API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Switch API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_device_switch_ports(self, serial: str) -> List[Dict[str, Any]]:
        """List the switch ports for a Meraki switch.

        Args:
            serial: Serial number of the Meraki switch.

        Returns:
            A list of dictionaries, where each dictionary represents a switch port.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/switch/ports"
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
                f"Unexpected error fetching switch ports for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching switch ports for device '{serial}': {e}"
            ) from e

    async def async_get_device_switch_port(
        self, serial: str, port_id: str
    ) -> Dict[str, Any]:
        """Return a switch port.

        Args:
            serial: Serial number of the Meraki switch.
            port_id: The ID of the switch port.

        Returns:
            A dictionary representing the specified switch port.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/switch/ports/{port_id}"
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
                f"Unexpected error fetching switch port '{port_id}' for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching switch port '{port_id}' for device '{serial}': {e}"
            ) from e

    async def async_get_network_switch_vlans(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the VLANs for a switch network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a VLAN.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/switch/vlans"
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
                f"Unexpected error fetching switch VLANs for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching switch VLANs for network '{network_id}': {e}"
            ) from e

    async def async_get_network_switch_vlan(
        self, network_id: str, vlan_id: str
    ) -> Dict[str, Any]:
        """Return a VLAN.

        Args:
            network_id: The ID of the Meraki network.
            vlan_id: The ID of the VLAN.

        Returns:
            A dictionary representing the specified VLAN.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/switch/vlans/{vlan_id}"
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
                f"Unexpected error fetching switch VLAN '{vlan_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching switch VLAN '{vlan_id}' for network '{network_id}': {e}"
            ) from e

    async def async_get_network_switch_stacks(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the switch stacks in a network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a switch stack.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/switch/stacks"
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
                f"Unexpected error fetching switch stacks for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching switch stacks for network '{network_id}': {e}"
            ) from e

    async def async_get_switch_stack(self, stack_id: str) -> Dict[str, Any]:
        """Return a switch stack.

        Args:
            stack_id: The ID of the switch stack.

        Returns:
            A dictionary representing the specified switch stack.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/switch/stacks/{stack_id}"
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
            _LOGGER.error(f"Unexpected error fetching switch stack '{stack_id}': {e}")
            raise MerakiApiError(
                f"Unexpected error fetching switch stack '{stack_id}': {e}"
            ) from e

    # Add other switch-related API calls here as needed.
    # Examples:
    # - async_get_network_switch_qos_rules(...)
    # - async_get_device_switch_lldp_cdp(...)
    # - async_get_network_switch_routing_interfaces(...)
