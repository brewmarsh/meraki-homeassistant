# /config/custom_components/meraki_ha/meraki_api/sensor.py
import logging
from typing import Any, Dict, List
from ._api_client import MerakiAPIClient

from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiSensorAPI:
    """Meraki sensor API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Sensor API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_network_sensors(self, network_id: str) -> List[Dict[str, Any]]:
        """List the sensors in a network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a sensor.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/sensors"
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
                f"Unexpected error fetching sensors for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching sensors for network '{network_id}': {e}"
            ) from e

    async def async_get_network_sensor(
        self, network_id: str, sensor_id: str
    ) -> Dict[str, Any]:
        """Return a sensor.

        Args:
            network_id: The ID of the Meraki network.
            sensor_id: The ID of the sensor.

        Returns:
            A dictionary representing the specified sensor.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/sensors/{sensor_id}"
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
                f"Unexpected error fetching sensor '{sensor_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching sensor '{sensor_id}' for network '{network_id}': {e}"
            ) from e

    async def async_get_device_sensor_relationships(
        self, serial: str
    ) -> List[Dict[str, Any]]:
        """List the sensor relationships of a sensor device.

        Args:
            serial: Serial number of the Meraki sensor device.

        Returns:
            A list of dictionaries, where each dictionary represents a sensor relationship.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/sensors/relationships"
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
                f"Unexpected error fetching sensor relationships for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching sensor relationships for device '{serial}': {e}"
            ) from e

    async def async_get_network_sensor_alerts_profiles(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List the alert profiles for a sensor network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a sensor alert profile.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/sensors/alerts/profiles"
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
                f"Unexpected error fetching sensor alert profiles for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching sensor alert profiles for network '{network_id}': {e}"
            ) from e

    async def async_get_network_sensor_alert_profile(
        self, network_id: str, profile_id: str
    ) -> Dict[str, Any]:
        """Return an alert profile for a sensor network.

        Args:
            network_id: The ID of the Meraki network.
            profile_id: The ID of the sensor alert profile.

        Returns:
            A dictionary representing the specified sensor alert profile.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/sensors/alerts/profiles/{profile_id}"
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
                f"Unexpected error fetching sensor alert profile '{profile_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching sensor alert profile '{profile_id}' for network '{network_id}': {e}"
            ) from e

    # Add other sensor-related API calls here as needed.
    # Examples:
    # - async_get_device_sensor_humidity(...)
    # - async_get_network_sensor_data(...)
    # - async_get_device_sensor_temperature(...)
