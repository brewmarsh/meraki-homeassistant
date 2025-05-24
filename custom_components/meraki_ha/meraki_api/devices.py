# /config/custom_components/meraki_ha/meraki_api/devices.py
import asyncio
import logging
from typing import Any, Dict, List, Optional
import json  # Keep json import

from ._api_client import MerakiAPIClient

from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha devices.py loaded")


class MerakiDevicesAPI:
    """Meraki devices API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Devices API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_organization_devices(
        self, organization_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Retrieves all devices from a Meraki organization.

        Args:
            organization_id: The ID of the Meraki organization.

        Returns:
            A list of dictionaries, where each dictionary represents a Meraki device,
            or None if an error occurs.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        _LOGGER.debug(f"Retrieving Meraki devices for Org ID: {organization_id}")
        endpoint = f"/organizations/{organization_id}/devices"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            data = await self._client._async_meraki_request("GET", url, headers)
            _LOGGER.debug(f"Raw Meraki API response: {json.dumps(data)}")
            devices: List[Dict[str, Any]] = []
            for device in data:
                _LOGGER.debug(f"Device before processing: {device}")
                device_data = {}
                for key, value in device.items():
                    if key is not None:
                        device_data[key] = value
                    else:
                        _LOGGER.warning(f"Found None key in device data: {device}")
                devices.append(device_data)
                _LOGGER.debug(f"Device after processing: {device_data}")
                await asyncio.sleep(0.1)  # Reduced sleep time, consider if needed
            return devices
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error retrieving Meraki devices for organization '{organization_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving Meraki devices for organization '{organization_id}': {e}"
            ) from e

    async def async_get_network_clients(self, network_id: str) -> List[Dict[str, Any]]:
        """Retrieve connected clients for a specific Meraki network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a connected client.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/clients"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Retrieving Meraki clients for network: {network_id}")
        try:
            data = await self._client._async_meraki_request("GET", url, headers)
            _LOGGER.debug(f"Meraki API response: {data}")
            return data
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error retrieving clients for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving clients for network '{network_id}': {e}"
            ) from e

    async def async_get_device_tags(self, serial: str) -> Optional[List[str]]:
        """Retrieves the tags for a specific Meraki device.

        Args:
            serial: Serial number of the Meraki device.

        Returns:
            A list of tag strings for the device, or None if an error occurs.
            Returns an empty list if tags are not found (HTTP 404).

        Raises:
            MerakiApiError: If an error occurs during the API call (excluding 404).
        """
        endpoint = f"/devices/{serial}/tags"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Retrieving tags for device serial: {serial}")
        try:
            data = await self._client._async_meraki_request("GET", url, headers)
            _LOGGER.debug(f"Meraki API response: {data}")
            return data  # Assuming the API returns a list of tag strings
        except MerakiApiError as e:
            if e.status_code == 404:
                _LOGGER.warning(f"Device tags not found for device {serial}.")
                return []
            else:
                _LOGGER.error(
                    f"Failed to retrieve device tags for device {serial}. Status: {e.status_code}, Text: {e.message}"
                )
                raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error retrieving device tags for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving device tags for device '{serial}': {e}"
            ) from e

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> bool:
        """Updates the tags for a specific Meraki device.

        Args:
            serial: Serial number of the Meraki device.
            tags: A list of tags to set for the device.

        Returns:
            True if the tags were updated successfully.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/tags"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"Updating tags for device serial: {serial} with tags: {tags}")
        payload = {"tags": tags}
        try:
            await self._client._async_meraki_request("PUT", url, headers, json=payload)
            _LOGGER.debug("Device tags updated successfully")
            return True
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error updating device tags for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error updating device tags for device '{serial}': {e}"
            ) from e

    async def async_get_device(self, serial: str) -> Optional[Dict[str, Any]]:
        """Retrieve details for a specific Meraki device.

        Args:
            serial: Serial number of the Meraki device.

        Returns:
            A dictionary containing the details of the Meraki device,
            or None if an error occurs.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}"
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
                f"Unexpected error retrieving device details for serial '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving device details for serial '{serial}': {e}"
            ) from e

    # Add other device-related API calls here as needed.
    # Examples:
    # - async_reboot_device(...)
    # - async_blink_device_leds(...)
