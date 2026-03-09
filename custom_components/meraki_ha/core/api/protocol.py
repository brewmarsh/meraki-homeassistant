"""Protocol for Meraki API Client."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

import meraki


class ApplianceEndpointsProtocol(Protocol):
    """Protocol for appliance endpoints."""

    async def get_l3_firewall_rules(self, network_id: str) -> dict[str, Any]:
        """Get L3 firewall rules for a network."""
        ...

    async def update_l3_firewall_rules(
        self, network_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update L3 firewall rules for a network."""
        ...

    async def get_network_appliance_l7_firewall_rules(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get L7 firewall rules for a network."""
        ...

    async def update_network_appliance_l7_firewall_rules(
        self, network_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update L7 firewall rules for a network."""
        ...

    async def get_network_appliance_content_filtering(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get content filtering settings for a network."""
        ...

    async def get_network_appliance_content_filtering_categories(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get content filtering categories for a network."""
        ...

    async def update_network_appliance_content_filtering(
        self, network_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update content filtering for a network."""
        ...

    async def get_network_vlans(self, network_id: str) -> list[dict[str, Any]]:
        """Get VLANs for a network."""
        ...

    async def update_network_vlan(
        self, network_id: str, vlan_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update a VLAN."""
        ...

    async def reboot_device(self, serial: str) -> dict[str, Any]:
        """Reboot a device."""
        ...

    async def update_network_appliance_port(
        self, network_id: str, port_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update an appliance port."""
        ...

    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """Get all ports for an appliance."""
        ...

    async def get_network_appliance_settings(self, network_id: str) -> dict[str, Any]:
        """Get settings for a network appliance."""
        ...

    async def get_network_appliance_traffic(
        self, network_id: str, timespan: int = 86400
    ) -> list[dict[str, Any]]:
        """Get traffic data for a network appliance."""
        ...

    async def get_traffic_shaping(self, network_id: str) -> dict[str, Any]:
        """Get traffic shaping settings for a network."""
        ...

    async def update_traffic_shaping(
        self, network_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update traffic shaping settings for a network."""
        ...

    async def get_device_appliance_uplinks_settings(
        self, serial: str
    ) -> dict[str, Any]:
        """Get uplinks settings for a device."""
        ...

    async def get_network_appliance_uplinks_performance(
        self, network_id: str
    ) -> list[dict[str, Any]]:
        """Get uplink performance for all devices in a network."""
        ...

    async def get_organization_appliance_uplink_statuses(self) -> list[dict[str, Any]]:
        """Get uplink status for all appliances in the organization."""
        ...

    async def get_vpn_status(self, network_id: str) -> dict[str, Any]:
        """Get site-to-site VPN status for a network."""
        ...

    async def update_vpn_status(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update site-to-site VPN status for a network."""
        ...


class CameraEndpointsProtocol(Protocol):
    """Protocol for camera endpoints."""

    async def get_camera_sense_settings(self, serial: str) -> dict[str, Any]:
        """Get sense settings for a specific camera."""
        ...

    async def get_camera_video_settings(self, serial: str) -> dict[str, Any]:
        """Get video settings for a specific camera."""
        ...

    async def get_device_camera_video_link(self, serial: str) -> dict[str, Any]:
        """Get video link for a specific camera."""
        ...

    async def update_camera_video_settings(
        self, serial: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update video settings for a specific camera."""
        ...

    async def update_camera_sense_settings(
        self, serial: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update sense settings for a specific camera."""
        ...

    async def get_device_camera_analytics_recent(
        self, serial: str, object_type: str = "person"
    ) -> list[dict[str, Any]]:
        """Get recent analytics for a specific camera."""
        ...

    async def get_device_camera_analytics_zones(
        self, serial: str
    ) -> list[dict[str, Any]]:
        """Get analytics zones for a specific camera."""
        ...

    async def generate_device_camera_snapshot(
        self, serial: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Generate a snapshot of what the camera sees."""
        ...


class DevicesEndpointsProtocol(Protocol):
    """Protocol for devices endpoints."""

    async def get_device_clients(self, serial: str) -> list[dict[str, Any]]:
        """Get all clients for a device."""
        ...

    async def get_device(self, serial: str) -> dict[str, Any]:
        """Get a single device."""
        ...

    async def update_device(self, serial: str, **kwargs: Any) -> dict[str, Any]:
        """Update a device."""
        ...

    async def get_device_management_interface(self, serial: str) -> dict[str, Any]:
        """Get the management interface for a device."""
        ...

    async def update_device_management_interface(
        self, serial: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update the management interface for a device."""
        ...


class NetworkEndpointsProtocol(Protocol):
    """Protocol for network endpoints."""

    async def get_network_clients(
        self,
        network_id: str,
        timespan: int | None = None,
        perPage: int | None = None,
        statuses: list[str] | None = None,
        total_pages: int | str = "all",
    ) -> list[dict[str, Any]]:
        """Get all clients in a network."""
        ...

    async def get_network_traffic(
        self, network_id: str, device_type: str
    ) -> list[dict[str, Any]]:
        """Get traffic data for a network, filtered by device type."""
        ...

    async def get_webhooks(self, network_id: str) -> list[dict[str, Any]]:
        """Get all webhooks for a network."""
        ...

    async def delete_webhook(self, network_id: str, webhook_id: str) -> None:
        """Delete a webhook from a network."""
        ...

    async def find_webhook_by_name_and_url(
        self, network_id: str, name: str, url: str
    ) -> dict[str, Any] | None:
        """Find a webhook by its name and URL."""
        ...

    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> list[str]:
        """Register or update a webhook with the Meraki API."""
        ...

    async def unregister_webhook(self, config_entry_id: str) -> None:
        """Unregister a webhook from all networks."""
        ...

    async def get_vlan_data(self, network_id: str) -> list[dict[str, Any]]:
        """Get VLAN data for a network with fallback and safety logic."""
        ...

    async def get_group_policies(self, network_id: str) -> list[dict[str, Any]]:
        """Get group policies for a network."""
        ...

    async def get_network_events(
        self, network_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Fetch events for a network."""
        ...


class OrganizationEndpointsProtocol(Protocol):
    """Protocol for organization endpoints needed by the API Client."""

    async def get_organization(self) -> dict[str, Any]:
        """Get organization details."""
        ...

    async def get_organization_networks(self) -> list[dict[str, Any]]:
        """Get all networks for an organization."""
        ...

    async def get_organization_firmware_upgrades(self) -> list[dict[str, Any]]:
        """Get firmware upgrade status for the organization."""
        ...

    async def get_organization_devices_statuses(self) -> list[dict[str, Any]]:
        """Get status information for all devices in the organization."""
        ...

    async def get_organization_devices_availabilities(self) -> list[dict[str, Any]]:
        """Get availability information for all devices in the organization."""
        ...

    async def get_organization_devices(self) -> list[dict[str, Any]]:
        """Get all devices in the organization."""
        ...

    async def get_organizations(self) -> list[dict[str, Any]]:
        """Get all organizations accessible by the API key."""
        ...

    async def get_organization_wireless_ssids_statuses_by_device(
        self,
    ) -> list[dict[str, Any]]:
        """Get organization-wide wireless SSIDs statuses by device."""
        ...

    async def get_organization_switch_ports_statuses(self) -> list[dict[str, Any]]:
        """Get organization-wide switch ports statuses."""
        ...


class SwitchEndpointsProtocol(Protocol):
    """Protocol for switch endpoints."""

    async def get_device_switch_ports_statuses(
        self, serial: str
    ) -> list[dict[str, Any]]:
        """Get statuses for all ports of a switch."""
        ...

    async def get_switch_ports(self, serial: str) -> list[dict[str, Any]]:
        """Get ports for a switch."""
        ...

    async def cycle_device_switch_ports(
        self, serial: str, ports: list[str]
    ) -> dict[str, Any] | list[Any]:
        """Cycle a set of switch ports."""
        ...

    async def update_device_switch_port(
        self, serial: str, port_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update a switch port."""
        ...


class WirelessEndpointsProtocol(Protocol):
    """Protocol for wireless endpoints."""

    async def get_network_ssids(self, network_id: str) -> list[dict[str, Any]]:
        """Get all SSIDs for a network."""
        ...

    async def get_wireless_settings(self, serial: str) -> dict[str, Any]:
        """Get wireless radio settings for an access point."""
        ...

    async def get_network_wireless_ssid(
        self, network_id: str, number: str
    ) -> dict[str, Any]:
        """Get a single SSID."""
        ...

    async def update_network_wireless_ssid(
        self, network_id: str, number: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update an SSID."""
        ...

    async def get_network_wireless_rf_profiles(
        self, network_id: str
    ) -> list[dict[str, Any]]:
        """Get all RF profiles for a network."""
        ...

    async def get_network_wireless_ssid_l7_firewall_rules(
        self, network_id: str, number: str
    ) -> dict[str, Any]:
        """Get L7 firewall rules for an SSID."""
        ...

    def get_network_detail_tasks(
        self, network_id: str, product_types: list[str]
    ) -> dict[str, Any]:
        """Get tasks to fetch detailed data for a network."""
        ...

    def process_network_detail_data(
        self,
        detail_data: dict[str, Any],
        network_id: str,
        previous_data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Process the detailed data for a network."""
        ...

    async def create_identity_psk(
        self,
        network_id: str,
        number: str,
        name: str,
        group_policy_id: str | None = None,
        passphrase: str | None = None,
    ) -> dict[str, Any]:
        """Create an Identity PSK."""
        ...

    async def delete_identity_psk(
        self, network_id: str, number: str, identity_psk_id: str
    ) -> None:
        """Delete an Identity PSK."""
        ...

    async def update_network_wireless_ssid_l7_firewall_rules(
        self, network_id: str, number: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Update L7 firewall rules for an SSID."""
        ...


class SensorEndpointsProtocol(Protocol):
    """Protocol for sensor endpoints."""

    async def create_device_sensor_command(
        self, serial: str, operation: str
    ) -> dict[str, Any]:
        """Send a command to a sensor."""
        ...

    async def get_organization_sensor_readings_latest_for_serials(
        self, serials: list[str], metrics: list[str]
    ) -> list[dict[str, Any]]:
        """Return the latest readings for specified metrics from a list of sensors."""
        ...

    async def get_organization_sensor_readings_latest(self) -> list[dict[str, Any]]:
        """Return the latest available reading for each metric from each sensor."""
        ...

    async def get_device_sensor_relationships(
        self, serial: str
    ) -> list[dict[str, Any]]:
        """Return the sensor relationships for a device."""
        ...


class MerakiApiClientProtocol(Protocol):
    """Protocol defining the interface for the Meraki API Client."""

    @property
    def dashboard(self) -> meraki.DashboardAPI:
        """Get the Dashboard API instance."""
        ...

    @property
    def organization_id(self) -> str | None:
        """Get the organization ID."""
        ...

    @property
    def appliance(self) -> ApplianceEndpointsProtocol:
        """Get the appliance endpoints."""
        ...

    @property
    def camera(self) -> CameraEndpointsProtocol:
        """Get the camera endpoints."""
        ...

    @property
    def devices(self) -> DevicesEndpointsProtocol:
        """Get the devices endpoints."""
        ...

    @property
    def network(self) -> NetworkEndpointsProtocol:
        """Get the network endpoints."""
        ...

    @property
    def organization(self) -> OrganizationEndpointsProtocol:
        """Get the organization endpoints."""
        ...

    @property
    def switch(self) -> SwitchEndpointsProtocol:
        """Get the switch endpoints."""
        ...

    @property
    def wireless(self) -> WirelessEndpointsProtocol:
        """Get the wireless endpoints."""
        ...

    @property
    def sensor(self) -> SensorEndpointsProtocol:
        """Get the sensor endpoints."""
        ...

    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run a synchronous function in a thread pool."""
        ...

    async def run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """Run an awaitable with the semaphore."""
        ...

    def mark_feature_disabled(
        self, feature: str, network_id: str | None = None
    ) -> None:
        """Mark a feature as disabled for the current session."""
        ...

    def is_feature_disabled(self, feature: str, network_id: str | None = None) -> bool:
        """Check if a feature is disabled for the current session."""
        ...

    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> list[str]:
        """Register a webhook with the Meraki API."""
        ...

    async def unregister_webhook(self, config_entry_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        ...

    async def async_reboot_device(self, serial: str) -> dict[str, Any]:
        """Reboot a device."""
        ...

    async def async_get_switch_port_statuses(
        self,
        serial: str,
    ) -> list[dict[str, Any]]:
        """Get statuses for all ports of a switch."""
        ...

    async def async_cycle_switch_ports(
        self,
        serial: str,
        ports: list[str],
    ) -> dict[str, Any]:
        """Cycle a set of switch ports."""
        ...

    async def async_setup(self) -> None:
        """Perform asynchronous setup of the API client."""
        ...
