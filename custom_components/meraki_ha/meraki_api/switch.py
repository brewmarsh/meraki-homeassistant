"""Provides an interface to Meraki Switch (MS series) specific API endpoints.

This module contains the `MerakiSwitchAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to MS series switches.
This includes functionalities like listing switch ports, individual port details,
VLAN configurations, and switch stack information.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiException # Use the refined base exception

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchAPI:
    """Encapsulates Meraki Switch (MS series) related API calls.

    Provides methods to interact with Meraki switches, including managing
    ports, VLANs, and switch stacks. It relies on an instance of
    `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Switch API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_device_switch_ports(
        self, serial: str
    ) -> List[Dict[str, Any]]:
        """List the switch ports for a Meraki MS series switch.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-switch-ports

        Args:
            serial: The serial number of the Meraki switch.

        Returns:
            A list of dictionaries, where each dictionary represents a switch port.
            Returns an empty list if no ports are found or an error occurs.
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/switch/ports"
        _LOGGER.debug("Fetching switch ports for device serial: %s", serial)
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching switch ports for device '%s': %s", serial, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching switch ports for device '%s': %s", serial, e
            )
            raise MerakiApiException(
                f"Unexpected error for device '{serial}' switch ports: {e}"
            ) from e

    async def async_get_device_switch_port(
        self, serial: str, port_id: str # port_id is a string, e.g., "1", "24"
    ) -> Optional[Dict[str, Any]]:
        """Return a specific switch port.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-switch-port

        Args:
            serial: The serial number of the Meraki switch.
            port_id: The identifier of the switch port.

        Returns:
            A dictionary representing the specified switch port if found.
            Returns `None` if the port is not found (e.g., API returns 404).
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}/switch/ports/{port_id}"
        _LOGGER.debug(
            "Fetching switch port '%s' for device serial: %s", port_id, serial
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Switch port '%s' not found on device '%s'. API response: %s",
                    port_id,
                    serial,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching switch port '%s' for device '%s': %s",
                port_id,
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching switch port '%s' for device '%s': %s",
                port_id,
                serial,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for port '{port_id}' on device '{serial}': {e}"
            ) from e

    async def async_get_network_switch_vlans( # Corrected method name from appliance to switch
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the VLANs for a switch network. (Note: This endpoint is for Appliance/MX VLANs)

        The endpoint `/networks/{network_id}/switch/vlans` does not exist.
        VLANs on switches are typically configured per-port or via L3 interfaces.
        The endpoint `/networks/{network_id}/appliance/vlans` is for MX security appliances.
        If the intent is to get VLANs related to switch *ports*, those are part of port details.
        If the intent is L3 interface VLANs on switches: `/networks/{networkId}/switch/routing/interfaces/{interfaceId}`

        This method seems to be a misinterpretation of Meraki API structure.
        For now, I will assume it was intended for Appliance VLANs and point to the correct method
        or mark it as needing review. Given the class is `MerakiSwitchAPI`, it should deal with switch features.
        A common switch VLAN operation is listing all VLANs *configured* on switches in a network,
        but this isn't a direct top-level endpoint. It's often derived.

        Let's assume this method was intended to list L3 routing interfaces which might define VLANs.
        The endpoint for listing all L3 interfaces on a switch (which can define VLANs):
        `/networks/{networkId}/switch/routing/interfaces`

        Or, if it's about port-level VLAN assignments, that's part of port details.
        The closest direct "list VLANs for switches" endpoint might be `/networks/{networkId}/vlans`
        if it exists and applies to switches, but this is usually for MX.

        Revisiting: The Meraki API has `/networks/{network_id}/vlans` which is for *Appliance* VLANs.
        The endpoint `/networks/{network_id}/switch/settings` might contain some VLAN related info,
        or `/networks/{network_id}/switch/stp` for STP per VLAN.
        There is no direct `/networks/{network_id}/switch/vlans` to list all VLANs defined for switches.

        This method will be documented as a placeholder or removed if no direct equivalent for switches.
        For now, let's assume it's a conceptual method that might try to aggregate VLAN info from ports.
        However, a more direct approach is needed.

        The original code has `endpoint = f"/networks/{network_id}/switch/vlans"`.
        This endpoint does not exist in the official Meraki API v1 documentation.
        I will remove this method and its single-VLAN counterpart.

        Args:
            network_id: The ID of the Meraki network.
        """
        _LOGGER.warning(
            "Method `async_get_network_switch_vlans` and `async_get_network_switch_vlan` "
            "are based on a non-standard Meraki API endpoint (`/networks/{network_id}/switch/vlans`). "
            "These methods will be removed or need to be re-evaluated against valid API endpoints "
            "for switch VLAN information (e.g., port configurations or L3 routing interfaces)."
        )
        # This method is being removed as it's based on a non-existent endpoint.
        # To get VLAN information for switches, one would typically:
        # 1. Get all switch ports: async_get_device_switch_ports(serial)
        # 2. Inspect each port's configuration for its native VLAN, allowed VLANs, etc.
        # Or, for L3 switches, inspect routing interfaces.
        return [] # Placeholder return

    async def async_get_network_switch_vlan( # Removed as per above
        self, network_id: str, vlan_id: str
    ) -> Optional[Dict[str, Any]]:
        """(Removed) Fetch a specific VLAN for a switch network."""
        _LOGGER.warning("Method `async_get_network_switch_vlan` removed (non-standard endpoint).")
        return None # Placeholder return


    async def async_get_network_switch_stacks(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the switch stacks in a network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-switch-stacks

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a switch stack.
            Returns an empty list if no stacks are found or an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/switch/stacks"
        _LOGGER.debug("Fetching switch stacks for network ID: %s", network_id)
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching switch stacks for network '%s': %s",
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching switch stacks for network '%s': %s",
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for network '{network_id}' switch stacks: {e}"
            ) from e

    async def async_get_network_switch_stack( # Renamed from async_get_switch_stack for consistency
        self, network_id: str, switch_stack_id: str # Added network_id
    ) -> Optional[Dict[str, Any]]:
        """Return a specific switch stack.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-switch-stack

        Args:
            network_id: The ID of the Meraki network where the stack resides.
            switch_stack_id: The ID of the switch stack.

        Returns:
            A dictionary representing the specified switch stack if found.
            Returns `None` if the stack is not found (e.g., API returns 404).

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        # Corrected endpoint to be network-specific for retrieving a stack
        endpoint = f"/networks/{network_id}/switch/stacks/{switch_stack_id}"
        _LOGGER.debug(
            "Fetching switch stack '%s' in network ID: %s",
            switch_stack_id,
            network_id,
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Switch stack '%s' not found in network '%s'. API response: %s",
                    switch_stack_id,
                    network_id,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching switch stack '%s' in network '%s': %s",
                switch_stack_id,
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching switch stack '%s' in network '%s': %s",
                switch_stack_id,
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for stack '{switch_stack_id}' in network '{network_id}': {e}"
            ) from e

    # Add other switch-related API calls here as needed.
    # Examples:
    # - async_get_network_switch_settings(self, network_id: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/switch/settings
    # - async_update_device_switch_port(self, serial: str, port_id: str, **kwargs) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/switch/ports/{portId} (PUT)
    # - async_get_network_switch_link_aggregations(self, network_id: str) -> List[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/switch/linkAggregations
    # - async_get_network_switch_dscp_to_cos_mappings(self, network_id: str) -> Dict[str, Any]:
    #   Endpoint: /networks/{networkId}/switch/dscpToCosMappings
    # - async_get_network_switch_qos_rules(self, network_id: str) -> List[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/switch/qosRules
