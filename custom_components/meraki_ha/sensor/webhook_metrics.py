"""Webhook metrics sensor for monitoring and observability."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
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
    """Set up webhook metrics sensors from config entry."""
    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]
    webhook_manager = hass.data[DOMAIN][config_entry.entry_id].get("webhook_manager")

    if webhook_manager:
        sensors = [
            MerakiWebhookReceivedTotalSensor(coordinator, config_entry),
            MerakiWebhookProcessingDurationSensor(coordinator, config_entry),
            MerakiAPITargetedRefreshTotalSensor(coordinator, config_entry),
        ]
        async_add_entities(sensors, True)


class MerakiWebhookReceivedTotalSensor(CoordinatorEntity, SensorEntity):
    """Sensor tracking total webhooks received (counter)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "webhooks"

    # Type annotation for mypy - coordinator is MerakiDataCoordinator, not generic
    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the webhook counter sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_webhook_received_total"
        self._attr_name = "Webhook received total"

    @property
    def native_value(self) -> int:
        """Return total number of webhooks received."""
        return getattr(self.coordinator, "_webhook_received_count", 0)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._config_entry.options.get("enable_webhooks", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return breakdown by alert type."""
        attrs: dict[str, Any] = {}

        # Get webhook counts by alert type (if tracked)
        webhook_counts_by_type = getattr(
            self.coordinator, "_webhook_counts_by_type", {}
        )
        if webhook_counts_by_type:
            attrs["by_alert_type"] = dict(webhook_counts_by_type)

        # Rate metrics
        last_received = getattr(self.coordinator, "_last_webhook_received", None)
        if last_received:
            attrs["last_received"] = last_received.isoformat()

        return attrs

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:counter"

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


class MerakiWebhookProcessingDurationSensor(CoordinatorEntity, SensorEntity):
    """Sensor tracking webhook processing duration (histogram summary)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "ms"
    _attr_suggested_display_precision = 2

    # Type annotation for mypy - coordinator is MerakiDataCoordinator, not generic
    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the processing duration sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_webhook_processing_duration"
        self._attr_name = "Webhook processing duration"

    @property
    def native_value(self) -> float | None:
        """Return average processing duration in milliseconds."""
        durations = getattr(self.coordinator, "_webhook_processing_durations", [])
        if not durations:
            return None

        # Return average of last 100 durations
        recent_durations = durations[-100:]
        return sum(recent_durations) / len(recent_durations)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._config_entry.options.get("enable_webhooks", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return histogram-style metrics."""
        attrs: dict[str, Any] = {}
        durations = getattr(self.coordinator, "_webhook_processing_durations", [])

        if durations:
            recent = durations[-100:]  # Last 100 samples

            attrs["min_ms"] = round(min(recent), 2)
            attrs["max_ms"] = round(max(recent), 2)
            attrs["avg_ms"] = round(sum(recent) / len(recent), 2)

            # Percentiles
            sorted_durations = sorted(recent)
            attrs["p50_ms"] = round(sorted_durations[len(sorted_durations) // 2], 2)
            attrs["p95_ms"] = round(
                sorted_durations[int(len(sorted_durations) * 0.95)], 2
            )
            attrs["p99_ms"] = round(
                sorted_durations[int(len(sorted_durations) * 0.99)], 2
            )

            attrs["sample_count"] = len(recent)

            # Slow webhooks (>1 second)
            slow_count = sum(1 for d in recent if d > 1000)
            attrs["slow_webhooks_count"] = slow_count
            if slow_count > 0:
                attrs["slow_webhooks_percent"] = round(
                    (slow_count / len(recent)) * 100, 1
                )
        else:
            attrs["sample_count"] = 0

        return attrs

    @property
    def icon(self) -> str:
        """Return icon based on average duration."""
        avg = self.native_value
        if avg is None:
            return "mdi:timer-outline"

        if avg < 100:  # < 100ms - fast
            return "mdi:timer-check"
        if avg < 500:  # 100-500ms - normal
            return "mdi:timer"

        # > 500ms - slow
        return "mdi:timer-alert"

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


class MerakiAPITargetedRefreshTotalSensor(CoordinatorEntity, SensorEntity):
    """Sensor tracking API targeted refresh calls (counter by type)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "calls"

    # Type annotation for mypy - coordinator is MerakiDataCoordinator, not generic
    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the targeted refresh counter sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_api_targeted_refresh_total"
        self._attr_name = "API targeted refresh total"

    @property
    def native_value(self) -> int:
        """Return total number of targeted refresh API calls."""
        counts_by_type = getattr(
            self.coordinator, "_targeted_refresh_counts_by_type", {}
        )
        return sum(counts_by_type.values())

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._config_entry.options.get("enable_webhooks", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return breakdown by refresh type."""
        attrs: dict[str, Any] = {}

        # Counts by type (device, client, network, ssid)
        counts_by_type = getattr(
            self.coordinator, "_targeted_refresh_counts_by_type", {}
        )
        if counts_by_type:
            attrs["by_type"] = dict(counts_by_type)

        # Success/failure rates
        success_count = getattr(self.coordinator, "_targeted_refresh_success_count", 0)
        failure_count = getattr(self.coordinator, "_targeted_refresh_failure_count", 0)

        total = success_count + failure_count
        if total > 0:
            attrs["success_count"] = success_count
            attrs["failure_count"] = failure_count
            attrs["success_rate"] = round((success_count / total) * 100, 1)
        else:
            attrs["success_count"] = 0
            attrs["failure_count"] = 0
            attrs["success_rate"] = None

        # API call savings from webhooks
        if self._config_entry.options.get("webhook_polling_reduction", True):
            attrs["polling_reduction_active"] = True
            # Estimated API calls saved per hour (rough estimate)
            # Without webhooks: ~54 calls/hour
            # With webhooks: ~8 calls/hour
            # Savings: ~46 calls/hour
            attrs["estimated_api_calls_saved_per_hour"] = 46
        else:
            attrs["polling_reduction_active"] = False

        return attrs

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:api"

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
