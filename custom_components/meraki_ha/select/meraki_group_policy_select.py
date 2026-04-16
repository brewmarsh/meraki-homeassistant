"""Select entity for controlling Meraki Group Policies."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.select import SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo

from ..entity import MerakiSelect

if TYPE_CHECKING:
    from ..coordinators import MerakiMainCoordinator
    from ..core.api import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class MerakiGroupPolicySelect(MerakiSelect):
    """Representation of a Meraki Group Policy select entity for an SSID."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        meraki_client: MerakiApiClientProtocol,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the Meraki Group Policy select entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._ssid_name = ssid_data.get("name")

        self.entity_description = SelectEntityDescription(
            key=f"group_policy_{self._network_id}_{self._ssid_number}",
            name=f"SSID {self._ssid_name} Group Policy",
            icon="mdi:account-group",
        )

        self._attr_unique_id = (
            f"meraki-ssid-{self._network_id}-{self._ssid_number}-group-policy"
        )
        self._update_options()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the network device."""
        from ..const.integration import DOMAIN

        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{self._network_id}")},
        )

    def _get_group_policies(self) -> list[dict[str, Any]]:
        """Get group policies for this network from static data."""
        return self.coordinator.static_data.get(
            f"group_policies_{self._network_id}", []
        )

    def _update_options(self) -> None:
        """Update available options from group policies."""
        policies = self._get_group_policies()
        # Default Meraki policies for SSIDs
        options = ["Allowed", "Blocked"]
        for policy in policies:
            if name := policy.get("name"):
                options.append(name)
        self._attr_options = options

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        ssid_data = self.coordinator.get_ssid(self._network_id, self._ssid_number)
        if not ssid_data:
            return None

        default_policy = ssid_data.get("defaultPolicy")
        if default_policy in ["Allowed", "Blocked"]:
            return default_policy

        if default_policy == "Group policy":
            group_policy_id = ssid_data.get("groupPolicyId")
            policies = self._get_group_policies()
            for policy in policies:
                if str(policy.get("groupPolicyId")) == str(group_policy_id):
                    return policy.get("name")

        return "Allowed"  # Default fallback

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        payload: dict[str, Any] = {}

        if option == "Allowed":
            payload["defaultPolicy"] = "Allowed"
        elif option == "Blocked":
            payload["defaultPolicy"] = "Blocked"
        else:
            # Must be a group policy name
            policies = self._get_group_policies()
            selected_policy = next(
                (p for p in policies if p.get("name") == option), None
            )
            if not selected_policy:
                raise ValueError(f"Invalid option: {option}")

            payload["defaultPolicy"] = "Group policy"
            payload["groupPolicyId"] = selected_policy["groupPolicyId"]

        try:
            await self._meraki_client.wireless.update_network_wireless_ssid(
                network_id=self._network_id,
                number=self._ssid_number,
                **payload,
            )
            # Update coordinator data optimistically or request refresh
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set group policy to '%s' for SSID %s: %s",
                option,
                self._ssid_name,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set group policy to '{option}': {e}"
            ) from e

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_options()
        self.async_write_ha_state()
