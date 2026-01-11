"""Meraki API endpoints for organizations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ....async_logging import async_log_time
from ....helpers.logging_helper import MerakiLoggers
from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = MerakiLoggers.API


class OrganizationEndpoints:
    """Organization-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization(self) -> dict[str, Any]:
        """
        Get organization details.

        Returns
        -------
            The organization details.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.organizations
        org = await api.getOrganization(
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(org)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_organization did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    @async_log_time(slow_threshold=2.0)
    async def get_organization_networks(self) -> list[dict[str, Any]]:
        """
        Get all networks for an organization.

        Returns
        -------
            A list of networks.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        networks = await api.getOrganizationNetworks(
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(networks)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_networks did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_organization_firmware_upgrades(self) -> list[dict[str, Any]]:
        """
        Get firmware upgrade status for the organization.

        Returns
        -------
            A list of firmware upgrades.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        upgrades = await api.getOrganizationFirmwareUpgrades(
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(upgrades)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_firmware_upgrades did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    @async_log_time(slow_threshold=3.0)
    async def get_organization_device_statuses(self) -> list[dict[str, Any]]:
        """
        Get status information for all devices in the organization.

        Returns
        -------
            A list of device statuses.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        statuses = await api.getOrganizationDeviceStatuses(
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_device_statuses did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    @async_log_time(slow_threshold=3.0)
    async def get_organization_devices_availabilities(self) -> list[dict[str, Any]]:
        """
        Get availability information for all devices in the organization.

        Returns
        -------
            A list of device availabilities.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        availabilities = await api.getOrganizationDevicesAvailabilities(
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(availabilities)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_devices_availabilities did not return a list."
            )
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    @async_log_time(slow_threshold=3.0)
    async def get_organization_devices(self) -> list[dict[str, Any]]:
        """
        Get all devices in the organization.

        Returns
        -------
            A list of devices.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        devices = await api.getOrganizationDevices(
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(devices)
        if not isinstance(validated, list):
            _LOGGER.warning("get_devices did not return a list, returning empty list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organizations(self) -> list[dict[str, Any]]:
        """
        Get all organizations accessible by the API key.

        Returns
        -------
            A list of organizations.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.organizations
        orgs = await api.getOrganizations()
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organizations did not return a list.")
            return []
        return validated
