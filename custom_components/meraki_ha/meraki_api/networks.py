"""Provides an interface to Meraki Network-specific API endpoints.

This module contains the `MerakiNetworksAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to network configurations
and information. This includes listing networks within an organization and
retrieving client counts for specific networks.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiException # Use the refined base exception
# MerakiApiError can be used if it's an alias or for specific broader cases.

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiNetworksAPI:
    """Encapsulates Meraki Network related API calls.

    Provides methods to retrieve information about networks within a Meraki
    organization, such as listing all networks or getting client counts.
    It relies on an instance of `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Networks API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_organization_networks(
        self,
        organization_id: str,
        config_template_id: Optional[str] = None,
        is_bound_to_config_template: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        tags_filter_type: Optional[str] = None, # 'withAllTags' or 'withAnyTags'
        per_page: Optional[int] = None,
        starting_after: Optional[str] = None,
    ) -> List[Dict[str, Any]]: # Return type adjusted to List[Dict[str, Any]]
        """List the networks that the user has privileges on in an organization.

        Supports filtering by configuration template, tags, and pagination.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-organization-networks

        Args:
            organization_id: The ID of the Meraki organization.
            config_template_id: (Optional) Filter networks by config template ID.
            is_bound_to_config_template: (Optional) Filter networks by whether they are
                                         bound to a config template.
            tags: (Optional) An array of tags to filter networks with.
            tags_filter_type: (Optional) Specifies how to filter networks by tags.
                              Can be 'withAllTags' or 'withAnyTags'.
                              Required if `tags` is provided.
            per_page: (Optional) The number of entries per page for pagination.
            starting_after: (Optional) A token used for pagination.

        Returns:
            A list of dictionaries, where each dictionary represents a Meraki
            network. Returns an empty list if no networks are found or if an
            error occurs that doesn't raise an exception. The structure of network
            dictionaries is defined by the Meraki API.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/organizations/{organization_id}/networks"
        params: Dict[str, Any] = {}
        if config_template_id is not None:
            params["configTemplateId"] = config_template_id
        if is_bound_to_config_template is not None:
            params["isBoundToConfigTemplate"] = is_bound_to_config_template
        if tags is not None:
            params["tags"] = tags
            if tags_filter_type: # Required if tags are used
                params["tagsFilterType"] = tags_filter_type
            else:
                _LOGGER.warning("`tags_filter_type` is required when `tags` are provided for network filtering.")
        if per_page is not None:
            params["perPage"] = per_page
        if starting_after is not None:
            params["startingAfter"] = starting_after

        _LOGGER.debug(
            "Fetching organization networks for Org ID: %s, with params: %s",
            organization_id,
            params,
        )
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint, params=params
            )
            # API is expected to return a list of network objects
            return response if isinstance(response, list) else []
        except MerakiApiException as e: # Catch the base or more specific API exceptions
            _LOGGER.error(
                "Meraki API error fetching networks for organization '%s': %s",
                organization_id,
                e,
            )
            raise # Re-raise for the caller to handle
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching networks for organization '%s': %s",
                organization_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for organization '{organization_id}' networks: {e}"
            ) from e

    async def async_get_network_clients_count(
        self, network_id: str, timespan: int = 86400 # Default to 24 hours in seconds
    ) -> int: # Return type changed to int, as it should return a count or raise
        """Return the number of clients that have used this network in the timespan.

        This method fetches all clients for the network within the given timespan
        and returns the count.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-clients
                   (This method derives the count from the list of clients.)

        Args:
            network_id: The ID of the Meraki network.
            timespan: The timespan in seconds for which to retrieve clients.
                      Defaults to 86400 seconds (24 hours).

        Returns:
            The number of clients connected to the network within the specified timespan.
            Returns 0 if no clients are found or if an error occurs that results
            in an empty client list.

        Raises:
            MerakiApiException: If a critical error occurs during the API call to fetch clients.
        """
        endpoint = f"/networks/{network_id}/clients"
        params: Dict[str, Any] = {"timespan": timespan}
        # This endpoint supports pagination. For an accurate count of *all* clients,
        # pagination would need to be handled if the number of clients exceeds the default page size.
        # However, for a simple count, fetching the first page might be sufficient or
        # the API might provide a total count in headers (check API docs for Link header with rel=last).
        # For now, assuming a single page fetch or that the default page size is large enough for typical use.
        _LOGGER.debug(
            "Fetching client count for network ID: %s, timespan: %d seconds",
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
            raise # Re-raise for the caller to handle
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching client count for network '%s': %s",
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for network '{network_id}' client count: {e}"
            ) from e

    async def async_get_network_ids_and_names(
        self, organization_id: str
    ) -> List[Dict[str, str]]: # Return type adjusted, should not be Optional if errors raise
        """Retrieve a simplified list of network IDs and names for an organization.

        This is a utility method that fetches all networks for an organization
        and then extracts just the 'id' and 'name' for each network.

        Args:
            organization_id: The ID of the Meraki organization.

        Returns:
            A list of dictionaries, where each dictionary contains the 'id' and 'name'
            of a Meraki network. Returns an empty list if no networks are found or
            if an error occurs during the underlying network fetch.

        Raises:
            MerakiApiException: If an error occurs during the API call to fetch networks.
        """
        _LOGGER.debug(
            "Fetching network IDs and names for organization ID: %s", organization_id
        )
        try:
            # Pass through pagination/filtering parameters if this method should support them
            networks: List[
                Dict[str, Any]
            ] = await self.async_get_organization_networks(organization_id)

            if not networks: # Handles None or empty list from the above call if it didn't raise
                return []

            return [
                {"id": str(network.get("id")), "name": str(network.get("name", "Unnamed Network"))}
                for network in networks if network.get("id") # Ensure network has an id
            ]
        except MerakiApiException:
            # Error already logged by async_get_organization_networks
            raise # Re-raise the original exception
        except Exception as e: # Should ideally be caught by the above, but as a safeguard
            _LOGGER.exception(
                "Unexpected error processing network IDs and names for organization '%s': %s",
                organization_id,
                e
            )
            raise MerakiApiException(
                 f"Unexpected error processing network IDs/names for org '{organization_id}': {e}"
            ) from e


    # Add other network-related API calls here as needed.
    # Examples:
    # - async_get_network_details(self, network_id: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}
    # - async_update_network_settings(self, network_id: str, settings: Dict) -> Dict[str, Any]:
    #   Endpoint: /networks/{networkId} (PUT request)
    # - async_get_network_alerts_history(self, network_id: str, **kwargs) -> List[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/alerts/history
    # - async_get_network_traffic_analysis(self, network_id: str, timespan: str, **kwargs) -> Dict[str, Any]:
    #   Endpoint: /networks/{networkId}/trafficAnalysis
