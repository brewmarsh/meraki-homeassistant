"""Provider for wireless radio entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.const import EntityCategory

from ...sensor.device.wireless_radio import MerakiWirelessRadioSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...core.models.device import MerakiDevice
    from ..coordinators import MerakiMainCoordinator

_LOGGER = logging.getLogger(__name__)


class WirelessRadioProvider:
    """Provider for wireless radio entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities for wireless radio settings (Channels and Power)."""
        if not device.serial or not device.wireless_radio_settings:
            return []

        entities: list[Entity] = []
        settings = device.wireless_radio_settings

        # 1. 2.4GHz Channel
        if "twoFourGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="2.4ghz_channel",
                        name="2.4GHz channel",
                        icon="mdi:wifi",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "twoFourGhzSettings",
                    "channel",
                )
            )

        # 2. 5GHz Channel
        if "fiveGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="5ghz_channel",
                        name="5GHz channel",
                        icon="mdi:wifi",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "fiveGhzSettings",
                    "channel",
                )
            )

        # 3. 2.4GHz Target Power
        if "twoFourGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="2.4ghz_target_power",
                        name="2.4GHz target power",
                        native_unit_of_measurement="dBm",
                        icon="mdi:transmission-tower",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "twoFourGhzSettings",
                    "targetPower",
                )
            )

        # 4. 5GHz Target Power
        # Note: Kept as generic "Target power" for backward compatibility
        if "fiveGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="target_power",
                        name="Target power",
                        native_unit_of_measurement="dBm",
                        icon="mdi:transmission-tower",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "fiveGhzSettings",
                    "targetPower",
                )
            )

        return entities
