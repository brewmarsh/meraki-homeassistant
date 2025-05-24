"""Provides an interface to Meraki Sensor (MT series) specific API endpoints.

This module contains the `MerakiSensorAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to MT series environmental sensors.
This includes listing sensors, retrieving specific sensor details, sensor relationships,
and managing alert profiles.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .exceptions import MerakiApiException # Use the refined base exception

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiSensorAPI:
    """Encapsulates Meraki Sensor (MT series) related API calls.

    Provides methods to interact with Meraki environmental sensors, including
    listing sensors, fetching details, relationships, and alert profiles.
    It relies on an instance of `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Sensor API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_network_sensors( # This endpoint does not exist in Meraki v1 API.
        self, network_id: str                  # Sensors are devices, listed under /networks/{networkId}/devices or /organizations/{organizationId}/devices
    ) -> List[Dict[str, Any]]:
        """List the MT sensors in a network. (Conceptual - uses generic devices endpoint)

        Note: There isn't a direct `/networks/{network_id}/sensors` endpoint.
        This method would typically list all devices in a network and then filter
        for sensor models (e.g., models starting with "MT").
        Alternatively, sensors can be listed organization-wide and filtered.

        For this implementation, we'll assume it means listing devices and then
        the caller would filter, or use organization-level device listing with model filters.
        A more accurate Meraki approach is to get devices and check their model.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-devices

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a device
            that could be a sensor. Caller should filter by model (e.g., "MTxx").
            Returns an empty list if no devices are found or an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        # This is a common way to list devices that could be sensors.
        endpoint = f"/networks/{network_id}/devices"
        _LOGGER.debug(
            "Fetching all devices (to filter for sensors) for network ID: %s",
            network_id,
        )
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            # Caller should filter this list for models starting with "MT"
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching devices (for sensors) for network '%s': %s",
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching devices (for sensors) for network '%s': %s",
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for network '{network_id}' devices (sensors): {e}"
            ) from e

    async def async_get_device_sensor_details( # Renamed from get_network_sensor
        self, serial: str # Sensors are devices, identified by serial
    ) -> Optional[Dict[str, Any]]:
        """Return sensor details for a specific sensor device.

        Uses the generic device details endpoint.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device

        Args:
            serial: The serial number of the Meraki MT sensor device.

        Returns:
            A dictionary representing the specified sensor's details if found.
            Returns `None` if the sensor device is not found (e.g., API returns 404).

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}"
        _LOGGER.debug("Fetching details for sensor device serial: %s", serial)
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Sensor device with serial '%s' not found. API response: %s", serial, e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching details for sensor device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching details for sensor device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for sensor device '{serial}' details: {e}"
            ) from e

    async def async_get_device_sensor_relationships(
        self, serial: str
    ) -> List[Dict[str, Any]]:
        """List the sensor relationships for a given MT sensor device.

        Sensor relationships define which sensor metrics are reported by which sensor.
        For example, a temperature sensor might report temperature and humidity.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device-sensor-relationships

        Args:
            serial: The serial number of the Meraki MT sensor device.

        Returns:
            A list of dictionaries, where each dictionary describes a relationship
            between the device and a sensor metric (e.g., temperature, humidity).
            Returns an empty list if no relationships are found or an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/sensors/relationships"
        _LOGGER.debug(
            "Fetching sensor relationships for device serial: %s", serial
        )
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching sensor relationships for device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching sensor relationships for device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for device '{serial}' sensor relationships: {e}"
            ) from e

    async def async_get_network_sensor_alerts_profiles(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Lists all sensor alert profiles for a network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-sensor-alerts-profiles

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a sensor
            alert profile. Returns an empty list if no profiles are found or
            an error occurs.

        Raises:
            MerakiApiException: If a critical error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/sensors/alerts/profiles"
        _LOGGER.debug(
            "Fetching sensor alert profiles for network ID: %s", network_id
        )
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiException as e:
            _LOGGER.error(
                "Meraki API error fetching sensor alert profiles for network '%s': %s",
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching sensor alert profiles for network '%s': %s",
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for network '{network_id}' sensor alert profiles: {e}"
            ) from e

    async def async_get_network_sensor_alert_profile( # Corrected name from prior version
        self, network_id: str, profile_id: str # profile_id is 'id' from list profiles
    ) -> Optional[Dict[str, Any]]:
        """Show a sensor alert profile.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-sensor-alerts-profile

        Args:
            network_id: The ID of the Meraki network.
            profile_id: The ID of the sensor alert profile to retrieve.

        Returns:
            A dictionary representing the specified sensor alert profile if found.
            Returns `None` if the profile is not found (e.g., API returns 404).

        Raises:
            MerakiApiException: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/networks/{network_id}/sensors/alerts/profiles/{profile_id}"
        _LOGGER.debug(
            "Fetching sensor alert profile '%s' for network ID: %s",
            profile_id,
            network_id,
        )
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiException as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Sensor alert profile '%s' not found in network '%s'. API response: %s",
                    profile_id,
                    network_id,
                    e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching sensor alert profile '%s' for network '%s': %s",
                profile_id,
                network_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching sensor alert profile '%s' for network '%s': %s",
                profile_id,
                network_id,
                e,
            )
            raise MerakiApiException(
                f"Unexpected error for profile '{profile_id}' in network '{network_id}': {e}"
            ) from e

    # Add other sensor-related API calls here as needed.
    # Examples:
    # - async_get_device_sensor_command(self, serial: str, command_id: str) -> Dict[str, Any]:
    #   Endpoint: /devices/{serial}/sensors/commands/{commandId}
    # - async_get_device_sensor_commands(self, serial: str, **kwargs) -> List[Dict[str, Any]]:
    #   Endpoint: /devices/{serial}/sensors/commands
    # - async_get_network_sensor_mqtt_brokers(self, network_id: str) -> List[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/sensors/mqttBrokers
    # - async_get_organization_sensor_readings_history(self, organization_id: str, **kwargs) -> List[Dict[str, Any]]:
    #   Endpoint: /organizations/{organizationId}/sensors/readings/history
    # - async_get_organization_sensor_readings_latest(self, organization_id: str, **kwargs) -> List[Dict[str, Any]]:
    #   Endpoint: /organizations/{organizationId}/sensors/readings/latest
