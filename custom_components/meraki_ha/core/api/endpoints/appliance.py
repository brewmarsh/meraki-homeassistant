"""Meraki API endpoints for appliances."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from meraki.exceptions import AsyncAPIError

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ....core.errors import MerakiVlansDisabledError
from ....helpers.logging_helper import MerakiLoggers
from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = MerakiLoggers.API


class ApplianceEndpoints:
    """Appliance-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient, hass: HomeAssistant) -> None:
        """
        Initialize the endpoint.

        Args:
            api_client: The Meraki API client.
            hass: The Home Assistant instance.

        """
        self._api_client = api_client
        self._hass = hass

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_appliance_uplink_statuses(
        self,
    ) -> list[dict[str, Any]]:
        """
        Get uplink statuses for all appliances in the organization.

        Returns
        -------
            A list of appliance uplink statuses.

        """
        if self._api_client.dashboard is None:
            return []

        api = self._api_client.dashboard.appliance
        statuses = await api.getOrganizationApplianceUplinkStatuses(
            self._api_client.organization_id, total_pages="all"
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_appliance_uplink_statuses did not return a list"
            )
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_vlans(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get VLANs for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of VLANs.

        """
        if self._api_client.dashboard is None:
            return []
        try:
            vlans = await self._api_client.dashboard.appliance.getNetworkApplianceVlans(
                networkId=network_id,
            )
            validated = validate_response(vlans)
            if not isinstance(validated, list):
                _LOGGER.warning("get_network_vlans did not return a list")
                return []
            return validated
        except AsyncAPIError as e:
            if "VLANs are not enabled for this network" in str(e):
                raise MerakiVlansDisabledError from e
            raise

    @handle_meraki_errors
    async def update_network_vlan(
        self,
        network_id: str,
        vlan_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update a VLAN.

        Args:
            network_id: The ID of the network.
            vlan_id: The ID of the VLAN.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VLAN.

        """
        if self._api_client.dashboard is None:
            return {}
        vlan = await self._api_client.dashboard.appliance.updateNetworkApplianceVlan(
            networkId=network_id,
            vlanId=vlan_id,
            **kwargs,
        )
        validated = validate_response(vlan)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_vlan did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_l3_firewall_rules(self, network_id: str) -> dict[str, Any]:
        """
        Get L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L3 firewall rules.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        rules = await api.getNetworkApplianceFirewallL3FirewallRules(
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_l3_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L3 firewall rules.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        rules = await api.updateNetworkApplianceFirewallL3FirewallRules(
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_traffic_shaping(self, network_id: str) -> dict[str, Any]:
        """
        Get traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The traffic shaping settings.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        settings = await api.getNetworkApplianceTrafficShaping(
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_traffic_shaping did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_traffic_shaping(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated traffic shaping settings.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        settings = await api.updateNetworkApplianceTrafficShaping(
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_traffic_shaping did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_vpn_status(self, network_id: str) -> dict[str, Any]:
        """
        Get site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The VPN status.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        status = await api.getNetworkApplianceVpnSiteToSiteVpn(
            networkId=network_id,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_vpn_status did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_vpn_status(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """
        Update site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VPN status.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        status = await api.updateNetworkApplianceVpnSiteToSiteVpn(
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_vpn_status did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_device_appliance_uplinks_settings(
        self,
        serial: str,
    ) -> dict[str, Any]:
        """
        Get uplinks settings for a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The uplinks settings.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        uplinks = await api.getDeviceApplianceUplinksSettings(
            serial=serial,
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_content_filtering(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering settings.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        result = await api.getNetworkApplianceContentFiltering(
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_content_filtering_categories(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering categories for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering categories.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        result = await api.getNetworkApplianceContentFilteringCategories(
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering_categories "
                "did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all ports for an appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of ports.

        """
        if self._api_client.dashboard is None:
            return []
        ports = await self._api_client.dashboard.appliance.getNetworkAppliancePorts(
            networkId=network_id,
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_appliance_ports did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_settings(self, network_id: str) -> dict[str, Any]:
        """
        Get settings for a network appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The settings for the network appliance.

        """
        if self._api_client.dashboard is None:
            return {}
        settings = (
            await self._api_client.dashboard.appliance.getNetworkApplianceSettings(
                networkId=network_id,
            )
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_appliance_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L7 firewall rules.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        rules = await api.getNetworkApplianceL7FirewallRules(
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L7 firewall rules.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        rules = await api.updateNetworkApplianceL7FirewallRules(
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_content_filtering(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update content filtering for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated content filtering settings.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.appliance
        result = await api.updateNetworkApplianceContentFiltering(
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated
