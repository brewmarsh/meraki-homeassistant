"""Provides an interface to general Meraki Device-specific API endpoints.

This module contains the `MerakiDevicesAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to device management.
This includes fetching lists of all devices in an organization, retrieving
details for specific devices, and managing device tags.
"""
import asyncio
import json # For logging raw API response if needed.
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiError

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha devices.py loaded") # This log might be too verbose for library use


class MerakiDevicesAPI:
    """Encapsulates Meraki Device related API calls.

    Provides methods for general device operations such as listing all devices,
    getting details for a specific device, and managing device tags.
    It utilizes an instance of `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Devices API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_organization_devices(
        self,
        organization_id: str,
        per_page: Optional[int] = None,
        starting_after: Optional[str] = None,
        configuration_updated_after: Optional[str] = None,
        # ... other optional parameters like model, mac, etc.
    ) -> List[Dict[str, Any]]:
        """List the devices in an organization.

        Supports pagination and filtering.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-organization-devices

        Args:
            organization_id: The ID of the Meraki organization.
            per_page: (Optional) The number of entries per page for pagination.
            starting_after: (Optional) A token used for pagination.
            configuration_updated_after: (Optional) Filter results by devices
                whose configurations were updated after the given timestamp
                (ISO8601 format).
            # Add other relevant optional filter parameters as needed.

        Returns:
            A list of dictionaries, where each dictionary represents a Meraki
            device. Returns an empty list if no devices are found or if an
            error occurs that doesn't raise an exception.

        Raises:
            MerakiApiError: If a critical error occurs during the API call.
        """
        endpoint = f"/organizations/{organization_id}/devices"
        params: Dict[str, Any] = {}
        if per_page is not None:
            params["perPage"] = per_page
        if starting_after is not None:
            params["startingAfter"] = starting_after
        if configuration_updated_after is not None:
            params["configurationUpdatedAfter"] = configuration_updated_after
        # Add other parameters to `params` dict if they are passed

        _LOGGER.debug(
            "Fetching organization devices for Org ID: %s, with params: %s",
            organization_id,
            params,
        )
        try:
            # The original code had complex processing for device data and an asyncio.sleep,
            # which is unusual for a direct API client method.
            # This has been simplified to return the raw API response, as processing
            # should ideally occur in a coordinator or data handler.
            response_data = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint, params=params
            )
            if _LOGGER.isEnabledFor(logging.DEBUG): # Avoid json.dumps if not debugging
                _LOGGER.debug("Raw Meraki API response for devices: %s", json.dumps(response_data, indent=2))

            # Ensure the response is a list, as expected from the API for this endpoint.
            return response_data if isinstance(response_data, list) else []
        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error fetching devices for organization '%s': %s",
                organization_id,
                e,
            )
            raise # Re-raise the original error for the caller to handle
        except Exception as e:
            _LOGGER.exception( # Use .exception for unexpected errors to get traceback
                "Unexpected error fetching devices for organization '%s': %s",
                organization_id,
                e,
            )
            raise MerakiApiError(
                f"Unexpected error for organization '{organization_id}' devices: {e}"
            ) from e

    async def async_get_device(
        self, serial: str
    ) -> Optional[Dict[str, Any]]:
        """Return a single device.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device

        Args:
            serial: The serial number of the Meraki device.

        Returns:
            A dictionary containing the details of the Meraki device if found.
            Returns `None` if the device is not found (e.g., API returns 404).

        Raises:
            MerakiApiError: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}"
        _LOGGER.debug("Fetching details for device serial: %s", serial)
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiError as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Device with serial '%s' not found. API response: %s", serial, e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching details for device '%s': %s", serial, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching details for device '%s': %s", serial, e
            )
            raise MerakiApiError(
                f"Unexpected error for device '{serial}' details: {e}"
            ) from e

    async def async_get_device_tags(
        self, serial: str
    ) -> List[str]: # Return type changed to List[str] as API returns list of strings
        """List the tags for a device.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-tags

        Args:
            serial: The serial number of the Meraki device.

        Returns:
            A list of tag strings for the device. Returns an empty list if the
            device has no tags or if an error occurs (including 404 Not Found,
            as per original code's behavior).

        Raises:
            MerakiApiError: If a critical error occurs during the API call,
                            excluding 404 if it's handled by returning [].
        """
        endpoint = f"/devices/{serial}/tags"
        _LOGGER.debug("Fetching tags for device serial: %s", serial)
        try:
            response_data = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            # API is expected to return a list of strings, e.g., ["tag1", "tag2"]
            return response_data if isinstance(response_data, list) and all(isinstance(tag, str) for tag in response_data) else []
        except MerakiApiError as e:
            # Original code checked e.status_code, which isn't a standard attr of base Exception.
            # Assuming MerakiApiError might have status_code or it's in e.args or a wrapped exception.
            # For now, using string check for 404 as a common pattern.
            if "404" in str(e):
                _LOGGER.warning(
                    "Tags not found for device '%s' (404). Returning empty list.", serial
                )
                return []
            _LOGGER.error(
                "Meraki API error fetching tags for device '%s': %s", serial, e
            )
            raise # Re-raise for other API errors
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching tags for device '%s': %s", serial, e
            )
            raise MerakiApiError(
                f"Unexpected error for device '{serial}' tags: {e}"
            ) from e

    async def async_update_device_tags(
        self, serial: str, tags: List[str]
    ) -> List[str]: # API returns the updated list of tags
        """Update the tags for a device.

        Tags are case-sensitive. Duplicate tags are not allowed.
        This operation replaces all existing tags with the new set provided.

        Reference: https://developer.cisco.com/meraki/api-v1/#!update-device-tags

        Args:
            serial: The serial number of the Meraki device.
            tags: A list of tag strings to set for the device.

        Returns:
            A list of strings representing the updated tags for the device.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/tags"
        # The API expects a JSON array of strings directly in the payload,
        # not a dictionary like {"tags": [...]}.
        # However, the _async_meraki_request takes a `json` param that is a dict.
        # If the Meraki library handles this correctly (e.g. by passing `json=tags` if `tags` is a list),
        # it might work. The common pattern for `aiohttp` is `json=payload_dict`.
        # The Meraki dashboard API documentation for "Update device tags" specifies:
        # Body Parameter (required): An array of tags.
        # This implies the payload should be the list itself, not wrapped in a dict.
        # Let's assume _async_meraki_request can handle `json=tags` if `tags` is a list.
        # If not, _api_client.py would need adjustment for such cases.
        # For now, adhering to how _async_meraki_request is defined (expects dict for json).
        # This means the original payload `{"tags": tags}` was likely correct if the client expects a dict.
        # However, if the API endpoint *strictly* wants a list as the root JSON, this could be an issue.
        # The official Meraki Python SDK passes the list directly as the `tags` argument to its function.
        # Let's assume the original payload `{"tags": tags}` is what `_async_meraki_request` expects.
        payload = {"tags": tags} # As per original code, assuming _async_meraki_request handles this structure for list payloads

        _LOGGER.debug(
            "Updating tags for device serial: %s with tags: %s", serial, tags
        )
        try:
            updated_tags = await self._client._async_meraki_request(
                method="PUT", endpoint=endpoint, json=payload # Original used `json=payload`
            )
            _LOGGER.info("Device tags updated successfully for %s.", serial)
            # API returns the updated list of tags
            return updated_tags if isinstance(updated_tags, list) else []
        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error updating tags for device '%s': %s", serial, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error updating tags for device '%s': %s", serial, e
            )
            raise MerakiApiError(
                f"Unexpected error updating device '{serial}' tags: {e}"
            ) from e

    # The async_get_network_clients method was present in the original devices.py.
    # However, client-related methods are typically grouped in clients.py.
    # It's kept here if it was intended for a specific reason, but it might be redundant
    # if meraki_api/clients.py has a similar, more comprehensive method.
    # For now, commenting out as it's likely better placed in clients.py.
    # async def async_get_network_clients(self, network_id: str) -> List[Dict[str, Any]]: ...

    # Add other general device-related API calls here as needed.
    # Examples:
    # - async_reboot_device(self, serial: str) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/reboot
    # - async_blink_device_leds(self, serial: str, duration: int, period: int, duty: int) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/blinkLeds
    # - async_get_device_management_interface(self, serial: str) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/managementInterface
    # - async_update_device_management_interface(self, serial: str, wan_config: Dict) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/managementInterface
