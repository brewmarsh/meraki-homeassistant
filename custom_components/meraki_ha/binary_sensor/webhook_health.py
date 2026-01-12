"""Webhook health diagnostic binary sensor."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up webhook health sensor from config entry."""
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]
    webhook_manager = hass.data[DOMAIN][config_entry.entry_id].get("webhook_manager")

    if webhook_manager:
        async_add_entities(
            [MerakiWebhookHealthSensor(coordinator, config_entry, webhook_manager)],
            True,
        )


class MerakiWebhookHealthSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor showing webhook health status."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True

    # Type annotation for mypy - coordinator is MerakiDataCoordinator, not generic
    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        webhook_manager: Any,
    ) -> None:
        """Initialize the webhook health sensor.

        Args:
        ----
            coordinator: The Meraki data coordinator.
            config_entry: The config entry.
            webhook_manager: The webhook manager instance.

        """
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._webhook_manager = webhook_manager
        self._attr_unique_id = f"{config_entry.entry_id}_webhook_health"
        self._attr_name = "Webhook health"

    @property
    def is_on(self) -> bool:
        """Return true if webhooks are healthy and receiving data.

        Webhooks are considered healthy if:
        1. Webhooks are enabled in configuration
        2. At least one webhook has been received
        3. A webhook was received within the last 15 minutes
        """
        if not self._config_entry.options.get("enable_webhooks", False):
            return False

        last_received = getattr(self.coordinator, "_last_webhook_received", None)
        if last_received is None:
            return False

        # Consider healthy if received within last 15 minutes
        age = (datetime.now() - last_received).total_seconds()
        return age < 900  # 15 minutes

    @property
    def available(self) -> bool:
        """Return if entity is available.

        Sensor is available if webhooks are enabled.
        """
        return self._config_entry.options.get("enable_webhooks", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes.

        Returns
        -------
            Dictionary of additional attributes including:
            - total_received: Total number of webhooks received
            - last_received: Timestamp of last webhook
            - registered_networks: Number of networks with webhooks registered
            - registration_errors: List of registration error messages
            - webhook_freshness: Age of last webhook in seconds
            - polling_reduction_active: Whether reduced polling is active

        """
        attrs: dict[str, Any] = {}

        # Webhook count
        attrs["total_received"] = getattr(
            self.coordinator, "_webhook_received_count", 0
        )

        # Last received timestamp
        last_received = getattr(self.coordinator, "_last_webhook_received", None)
        if last_received:
            attrs["last_received"] = last_received.isoformat()
            age_seconds = (datetime.now() - last_received).total_seconds()
            attrs["webhook_freshness_seconds"] = int(age_seconds)

            # Human-readable freshness
            if age_seconds < 60:
                attrs["last_received_ago"] = f"{int(age_seconds)} seconds ago"
            elif age_seconds < 3600:
                attrs["last_received_ago"] = f"{int(age_seconds / 60)} minutes ago"
            else:
                attrs["last_received_ago"] = f"{int(age_seconds / 3600)} hours ago"
        else:
            attrs["last_received"] = None
            attrs["webhook_freshness_seconds"] = None
            attrs["last_received_ago"] = "Never"

        # Registration status from webhook manager
        if self._webhook_manager:
            status = self._webhook_manager.webhook_status
            attrs["status"] = status.get("status", "unknown")
            attrs["status_message"] = status.get("message", "")

            # Registered networks
            http_server_ids = getattr(self._webhook_manager, "_http_server_ids", {})
            attrs["registered_networks"] = len(http_server_ids)

            # Registration errors
            errors = getattr(self._webhook_manager, "_registration_errors", [])
            if errors:
                attrs["registration_errors"] = errors
                attrs["has_registration_errors"] = True
            else:
                attrs["has_registration_errors"] = False

        # Polling reduction status
        polling_reduction_enabled = self._config_entry.options.get(
            "webhook_polling_reduction", True
        )
        attrs["polling_reduction_enabled"] = polling_reduction_enabled

        if polling_reduction_enabled and self.is_on:
            attrs["polling_reduction_active"] = True
        else:
            attrs["polling_reduction_active"] = False

        # Configuration
        attrs["webhook_auto_register"] = self._config_entry.options.get(
            "webhook_auto_register", True
        )

        alert_types = self._config_entry.options.get("webhook_alert_types", [])
        attrs["subscribed_alert_types"] = len(alert_types)

        return attrs

    @property
    def icon(self) -> str:
        """Return icon based on webhook health."""
        if not self.available:
            return "mdi:webhook-off"

        if self.is_on:
            return "mdi:webhook"

        # Enabled but not receiving
        return "mdi:webhook-off"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the organization."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"org_{self.coordinator.api.organization_id}")},
            name=self._config_entry.data.get(
                "org_name", f"Meraki Org {self.coordinator.api.organization_id}"
            ),
            manufacturer="Cisco Meraki",
            model="Organization",
        )
