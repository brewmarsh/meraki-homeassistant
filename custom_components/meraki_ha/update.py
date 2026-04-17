"""Update entity for Meraki devices."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityDescription,
    UpdateEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .coordinators.main import MerakiMainCoordinator
from .core.models.device import MerakiDevice
from .entity import MerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiUpdateEntity(MerakiEntity[MerakiMainCoordinator], UpdateEntity):
    """Update entity for a Meraki device."""

    _attr_has_entity_name = True
    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_supported_features = (
        UpdateEntityFeature.INSTALL | UpdateEntityFeature.RELEASE_NOTES
    )

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the update entity."""
        super().__init__(coordinator)
        self._device = device
        self._config_entry = config_entry
        self._attr_unique_id = f"{device.serial}_update"
        self.entity_description = UpdateEntityDescription(
            key="update",
            name="Firmware Update",
        )

    @property
    def installed_version(self) -> str | None:
        """Return the current installed version."""
        device = self.device_data
        if not device:
            return None
        return getattr(device, "firmware", None)

    @property
    def latest_version(self) -> str | None:
        """Return the latest available version."""
        device = self.device_data
        if not device or not hasattr(device, "firmware_upgrades"):
            return self.installed_version

        upgrades = device.firmware_upgrades
        if not upgrades or not isinstance(upgrades, dict):
            return self.installed_version

        available_versions = upgrades.get("availableVersions")
        if not available_versions or not isinstance(available_versions, list):
            return self.installed_version

        # Get the latest version from the list
        # Meraki usually orders them by release date/priority
        latest = available_versions[0]
        if isinstance(latest, dict):
            return latest.get("firmware")

        return self.installed_version

    @property
    def release_notes(self) -> str | None:
        """Return the release notes for the latest version."""
        device = self.device_data
        if not device or not hasattr(device, "firmware_upgrades"):
            return None

        upgrades = device.firmware_upgrades
        if not upgrades or not isinstance(upgrades, dict):
            return None

        available_versions = upgrades.get("availableVersions")
        if not available_versions or not isinstance(available_versions, list):
            return None

        latest = available_versions[0]
        if isinstance(latest, dict):
            return latest.get("releaseNotes")

        return None

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Install an update."""
        device = self.device_data
        if not device or not device.network_id:
            raise HomeAssistantError("Device or network ID not found")

        try:
            # Trigger firmware upgrade for the network/product type
            # Meraki triggers upgrades per network/product
            # Note: We use the network-level API here
            await self.coordinator.api.network.create_network_firmware_upgrades_rollout(
                network_id=device.network_id,
                product_type=device.product_type,
            )
            # Request a refresh to update the status
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to trigger firmware upgrade: %s", err)
            raise HomeAssistantError(
                f"Failed to trigger firmware upgrade: {err}"
            ) from err
