"""Meraki API client wrapper."""

import asyncio
from functools import partial
import logging
from typing import Any, Dict, List, Optional
import time

import meraki  # type: ignore

from ..utils.api_utils import handle_meraki_errors, validate_response

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """Wrapper for the Meraki Dashboard API client.

    This client wraps the Meraki Python SDK to provide:
    - Async operation with proper threading
    - Consistent error handling and logging
    - Response validation and normalization
    - Intelligent caching with timeouts
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._org_id = org_id
        self._dashboard = meraki.DashboardAPI(
            api_key=api_key,
            base_url=base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

        # Initialize cache
        self._cache: Dict[str, Any] = {}
        self._cache_timeout = 300  # 5 minutes
        self._last_cache_update: Dict[str, float] = {}

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        _LOGGER.debug("Running synchronous function: %s", func.__name__)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    def _get_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate a cache key for a function call."""
        return f"{func_name}:{hash(str(args) + str(sorted(kwargs.items())))}"

    def _get_cached_data(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if it exists and is not expired."""
        if cache_key not in self._cache:
            return None

        last_update = self._last_cache_update.get(cache_key, 0)
        if time.time() - last_update > self._cache_timeout:
            return None

        return self._cache[cache_key]

    def _cache_data(self, cache_key: str, data: Any) -> None:
        """Cache data with current timestamp."""
        self._cache[cache_key] = data
        self._last_cache_update[cache_key] = time.time()

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    @handle_meraki_errors
    async def get_organization(self) -> Dict[str, Any]:
        """Get organization details."""
        _LOGGER.debug("Getting organization details")
        cache_key = self._get_cache_key("get_organization")

        if cached := self._get_cached_data(cache_key):
            return cached

        org = await self._run_sync(
            self._dashboard.organizations.getOrganization, organizationId=self._org_id
        )
        validated = validate_response(org)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations."""
        _LOGGER.debug("Getting all organizations")
        cache_key = self._get_cache_key("get_organizations")

        if cached := self._get_cached_data(cache_key):
            return cached

        orgs = await self._run_sync(self._dashboard.organizations.getOrganizations)
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organizations did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_network_clients(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all clients in a network."""
        _LOGGER.debug("Getting clients for network: %s", network_id)
        cache_key = self._get_cache_key("get_network_clients", network_id)

        # Client data should have a shorter cache timeout
        self._cache_timeout = 60  # 1 minute

        if cached := self._get_cached_data(cache_key):
            return cached

        clients = await self._run_sync(
            self._dashboard.networks.getNetworkClients, networkId=network_id
        )
        validated = validate_response(clients)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_network_clients did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)

        # Reset cache timeout
        self._cache_timeout = 300
        return validated

    @handle_meraki_errors
    async def get_networks(self) -> List[Dict[str, Any]]:
        """Get all networks in the organization."""
        _LOGGER.debug("Getting networks")
        cache_key = self._get_cache_key("get_networks")

        if cached := self._get_cached_data(cache_key):
            return cached

        networks = await self._run_sync(
            self._dashboard.organizations.getOrganizationNetworks,
            organizationId=self._org_id,
        )
        validated = validate_response(networks)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_networks did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_devices(
        self, network_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all devices in the organization or a specific network."""
        if network_id is None:
            _LOGGER.debug("Getting devices for entire organization")
        else:
            _LOGGER.debug("Getting devices for network: %s", network_id)

        cache_key = self._get_cache_key("get_devices", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        try:
            if network_id:
                devices = await self._run_sync(
                    self._dashboard.networks.getNetworkDevices, networkId=network_id
                )
            else:
                devices = await self._run_sync(
                    self._dashboard.organizations.getOrganizationDevices,
                    organizationId=self._org_id,
                )

            validated = validate_response(devices)
            if not isinstance(validated, list):
                _LOGGER.warning(
                    "get_devices did not return a list, returning empty list. Got: %s",
                    type(validated),
                )
                validated = []
            self._cache_data(cache_key, validated)
            return validated
        except Exception as err:
            _LOGGER.error("Error fetching devices: %s", err)
            return []

    @handle_meraki_errors
    async def get_camera_sense_settings(self, serial: str) -> Dict[str, Any]:
        """Get sense settings for a specific camera."""
        _LOGGER.debug("Getting camera sense settings for serial: %s", serial)
        cache_key = self._get_cache_key("get_camera_sense_settings", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        settings = await self._run_sync(
            self._dashboard.camera.getDeviceCameraSense, serial=serial
        )
        validated = validate_response(settings)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_camera_video_settings(self, serial: str) -> Dict[str, Any]:
        """Get video settings for a specific camera."""
        _LOGGER.debug("Getting camera video settings for serial: %s", serial)
        cache_key = self._get_cache_key("get_camera_video_settings", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        settings = await self._run_sync(
            self._dashboard.camera.getDeviceCameraVideoSettings, serial=serial
        )
        validated = validate_response(settings)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_device_camera_video_link(self, serial: str) -> Dict[str, Any]:
        """Get video link for a specific camera.

        Args:
            serial: The serial number of the camera.

        Returns:
            A dictionary containing the video link information.
        """
        _LOGGER.debug("Getting camera video link for serial: %s", serial)
        cache_key = self._get_cache_key("get_device_camera_video_link", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        link = await self._run_sync(
            self._dashboard.camera.getDeviceCameraVideoLink, serial=serial
        )
        validated = validate_response(link)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def update_camera_video_settings(self, serial: str, **kwargs) -> None:
        """Update video settings for a specific camera."""
        _LOGGER.debug("Updating camera video settings for serial: %s", serial)
        await self._run_sync(
            self._dashboard.camera.updateDeviceCameraVideoSettings,
            serial=serial,
            **kwargs,
        )

    @handle_meraki_errors
    async def update_network_wireless_ssid(
        self, network_id: str, number: str, **kwargs
    ) -> None:
        """Update a wireless SSID."""
        _LOGGER.debug(
            "Updating wireless SSID for network: %s, number: %s, with data: %s",
            network_id,
            number,
            kwargs,
        )
        # Create a dictionary of parameters to pass to the SDK
        params = {
            "networkId": network_id,
            "number": number,
        }
        if "name" in kwargs:
            params["name"] = kwargs["name"]
        if "enabled" in kwargs:
            params["enabled"] = kwargs["enabled"]
        if "broadcast" in kwargs:
            params["broadcast"] = kwargs["broadcast"]

        await self._run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsid,
            **params,
        )

    @handle_meraki_errors
    async def get_organization_firmware_upgrades(self) -> List[Dict[str, Any]]:
        """Get firmware upgrade status for the organization."""
        _LOGGER.debug("Getting organization firmware upgrades")
        cache_key = self._get_cache_key("get_organization_firmware_upgrades")

        if cached := self._get_cached_data(cache_key):
            return cached

        upgrades = await self._run_sync(
            self._dashboard.organizations.getOrganizationFirmwareUpgrades,
            organizationId=self._org_id,
        )
        validated = validate_response(upgrades)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_firmware_upgrades did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_organization_device_statuses(self) -> List[Dict[str, Any]]:
        """Get status information for all devices in the organization."""
        _LOGGER.debug("Getting device statuses for organization")
        cache_key = self._get_cache_key("get_organization_device_statuses")

        # Status data should have a shorter cache timeout
        self._cache_timeout = 60  # 1 minute

        if cached := self._get_cached_data(cache_key):
            return cached

        # Get device list first
        devices = await self.get_devices()
        statuses = []

        # Build status information from device data
        for device in devices:
            status = {
                "name": device.get("name"),
                "serial": device.get("serial"),
                "mac": device.get("mac"),
                "publicIp": device.get("lanIp"),  # Use lanIp as publicIp
                "status": device.get("status", "unknown"),
                "lastReportedAt": device.get("lastReportedAt"),
                "networkId": device.get("networkId"),
                "productType": device.get("productType", "unknown"),
            }
            statuses.append(status)

        self._cache_data(cache_key, statuses)

        # Reset cache timeout
        self._cache_timeout = 300
        return statuses

    @handle_meraki_errors
    async def get_device_clients(self, serial: str) -> List[Dict[str, Any]]:
        """Get client information for a specific device."""
        _LOGGER.debug("Getting device clients for serial: %s", serial)
        cache_key = self._get_cache_key("get_device_clients", serial)

        # Client data should have a shorter cache timeout
        self._cache_timeout = 60  # 1 minute

        if cached := self._get_cached_data(cache_key):
            return cached

        clients = await self._run_sync(
            self._dashboard.devices.getDeviceClients, serial=serial
        )
        validated = validate_response(clients)
        self._cache_data(cache_key, validated)

        # Reset cache timeout
        self._cache_timeout = 300
        return validated

    @handle_meraki_errors
    async def get_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get wireless SSIDs for a network."""
        _LOGGER.debug("Getting SSIDs for network: %s", network_id)
        cache_key = self._get_cache_key("get_ssids", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        ssids = await self._run_sync(
            self._dashboard.wireless.getNetworkWirelessSsids, networkId=network_id
        )
        validated = validate_response(ssids)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_network_appliance_traffic(
        self, network_id: str, timespan: int = 86400
    ) -> Dict[str, Any]:
        """Get traffic data for a network appliance.

        Args:
            network_id: The ID of the network.
            timespan: The timespan for which to retrieve traffic data, in seconds.

        Returns:
            A dictionary containing the traffic data.
        """
        _LOGGER.debug("Getting appliance traffic for network: %s", network_id)
        cache_key = self._get_cache_key(
            "get_network_appliance_traffic", network_id, timespan
        )

        if cached := self._get_cached_data(cache_key):
            return cached

        traffic = await self._run_sync(
            self._dashboard.devices.getNetworkApplianceTraffic,
            networkId=network_id,
            timespan=timespan,
        )
        validated = validate_response(traffic)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_vlans(self, network_id: str) -> List[Dict[str, Any]]:
        """Get VLANs for a network."""
        _LOGGER.debug("Getting VLANs for network: %s", network_id)
        cache_key = self._get_cache_key("get_vlans", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        vlans = await self._run_sync(
            self._dashboard.appliance.getNetworkApplianceVlans, networkId=network_id
        )
        validated = validate_response(vlans)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_device_appliance_uplinks_settings(
        self, serial: str
    ) -> Dict[str, Any]:
        """Get uplinks settings for a device.

        Args:
            serial: The serial number of the device.

        Returns:
            A dictionary representing the uplinks settings.
        """
        _LOGGER.debug("Getting uplinks settings for device: %s", serial)
        cache_key = self._get_cache_key(
            "get_device_appliance_uplinks_settings", serial
        )

        if cached := self._get_cached_data(cache_key):
            return cached

        uplinks = await self._run_sync(
            self._dashboard.appliance.getDeviceApplianceUplinksSettings, serial=serial
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict, returning empty dict. Got: %s",
                type(validated),
            )
            validated = {}
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_appliance_ports(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all ports for an appliance."""
        _LOGGER.debug("Getting appliance ports for network: %s", network_id)
        cache_key = self._get_cache_key("get_appliance_ports", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        ports = await self._run_sync(
            self._dashboard.appliance.getNetworkAppliancePorts, networkId=network_id
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_appliance_ports did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_device_switch_ports_statuses(
        self, serial: str
    ) -> List[Dict[str, Any]]:
        """Get statuses for all ports of a switch.

        Args:
            serial: The serial number of the switch.

        Returns:
            A list of dictionaries, each representing the status of a port.
        """
        _LOGGER.debug("Getting switch ports statuses for serial: %s", serial)
        cache_key = self._get_cache_key("get_device_switch_ports_statuses", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        statuses = await self._run_sync(
            self._dashboard.switch.getDeviceSwitchPortsStatuses, serial=serial
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_device_switch_ports_statuses did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_switch_ports(self, serial: str) -> List[Dict[str, Any]]:
        """Get ports for a switch."""
        _LOGGER.debug("Getting switch ports for serial: %s", serial)
        cache_key = self._get_cache_key("get_switch_ports", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        ports = await self._run_sync(
            self._dashboard.switch.getDeviceSwitchPorts, serial=serial
        )
        validated = validate_response(ports)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_device_sensor_readings(self, serial: str) -> List[Dict[str, Any]]:
        """Get readings for a sensor device.

        Args:
            serial: The serial number of the sensor device.

        Returns:
            A list of dictionaries, each representing a sensor reading.
        """
        _LOGGER.debug("Getting sensor readings for device: %s", serial)
        cache_key = self._get_cache_key("get_device_sensor_readings", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        readings = await self._run_sync(
            self._dashboard.devices.getDeviceSensorReadings, serial=serial
        )
        validated = validate_response(readings)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_device_sensor_readings did not return a list, returning empty list. Got: %s",
                type(validated),
            )
            validated = []
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_wireless_settings(self, serial: str) -> Dict[str, Any]:
        """Get wireless radio settings for an access point."""
        _LOGGER.debug("Getting wireless settings for serial: %s", serial)
        cache_key = self._get_cache_key("get_wireless_settings", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        settings = await self._run_sync(
            self._dashboard.wireless.getDeviceWirelessRadioSettings, serial=serial
        )
        validated = validate_response(settings)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API.

        If a webhook with the same URL already exists, it will be deleted and recreated
        to ensure the settings are up to date.
        """
        _LOGGER.debug("Registering webhook: %s", webhook_url)
        networks = await self.get_networks()

        for network in networks:
            network_id = network["id"]

            # Check if webhook already exists
            existing_webhook = await self.find_webhook_by_url(network_id, webhook_url)
            if existing_webhook:
                _LOGGER.debug(
                    "Found existing webhook with URL %s in network %s, updating...",
                    webhook_url,
                    network_id,
                )
                # Delete existing webhook
                await self.delete_webhook(network_id, existing_webhook["id"])

            # Create new webhook
            _LOGGER.debug("Creating webhook in network %s", network_id)
            await self._run_sync(
                self._dashboard.networks.createNetworkWebhooksHttpServer,
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=f"Home Assistant Integration - {network.get('name', 'Unknown')}",
            )

    @handle_meraki_errors
    async def unregister_webhook(self, webhook_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        _LOGGER.debug("Unregistering webhook: %s", webhook_id)
        networks = await self.get_networks()
        for network in networks:
            await self._run_sync(
                self._dashboard.networks.deleteNetworkWebhooksHttpServer,
                networkId=network["id"],
                httpServerId=webhook_id,
            )

    @handle_meraki_errors
    async def get_webhooks(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all webhooks for a network."""
        _LOGGER.debug("Getting webhooks for network %s", network_id)
        webhooks = await self._run_sync(
            self._dashboard.networks.getNetworkWebhooksHttpServers,
            networkId=network_id,
        )
        return validate_response(webhooks)

    @handle_meraki_errors
    async def delete_webhook(self, network_id: str, webhook_id: str) -> None:
        """Delete a webhook from a network."""
        _LOGGER.debug("Deleting webhook %s from network %s", webhook_id, network_id)
        await self._run_sync(
            self._dashboard.networks.deleteNetworkWebhooksHttpServer,
            networkId=network_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    async def find_webhook_by_url(
        self, network_id: str, url: str
    ) -> Optional[Dict[str, Any]]:
        """Find a webhook by its URL."""
        webhooks = await self.get_webhooks(network_id)
        for webhook in webhooks:
            if webhook.get("url") == url:
                return webhook
        return None
