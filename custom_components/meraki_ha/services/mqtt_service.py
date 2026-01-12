"""
MQTT Service for Meraki Integration.

This module handles subscribing to Meraki MQTT topics via Home Assistant's
MQTT integration and processing incoming sensor data.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from datetime import datetime
from functools import lru_cache
from typing import TYPE_CHECKING

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback

from ..const import MERAKI_MQTT_MT_TOPIC_PATTERN
from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator
    from .mqtt_relay import MqttRelayManager

# Use feature-specific logger - can be silenced independently via:
# logger:
#   logs:
#     custom_components.meraki_ha.mqtt: warning
_LOGGER = MerakiLoggers.MQTT

# Regex to parse Meraki MQTT topic structure
# Format: meraki/v1/mt/{network_id}/ble/{sensor_mac}/{metric}
MERAKI_MT_TOPIC_REGEX = re.compile(
    r"^meraki/v1/mt/(?P<network_id>[^/]+)/ble/(?P<sensor_mac>[^/]+)/(?P<metric>.+)$"
)


@lru_cache(maxsize=256)
def normalize_mac(mac: str) -> str:
    """
    Normalize MAC address to uppercase with colons.

    This function is memoized with LRU cache since MAC addresses are
    normalized on every MQTT message and the same sensors send repeatedly.

    Args:
    ----
        mac: MAC address in any format.

    Returns
    -------
        Normalized MAC address (e.g., "54:6C:0E:8A:9E:81").

    """
    # Remove any separators and convert to uppercase
    clean_mac = mac.upper().replace(":", "").replace("-", "").replace(".", "")
    # Insert colons every 2 characters
    return ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))


class MerakiMqttService:
    """
    Service for handling MQTT communication with Meraki devices.

    Subscribes to Meraki MQTT topics on HA's Mosquitto broker,
    parses incoming messages, and updates the coordinator with real-time data.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        relay_manager: MqttRelayManager | None = None,
    ) -> None:
        """
        Initialize the MQTT service.

        Args:
        ----
            hass: The Home Assistant instance.
            coordinator: The Meraki data coordinator.
            relay_manager: Optional relay manager for forwarding messages.

        """
        self._hass = hass
        self._coordinator = coordinator
        self._relay_manager = relay_manager
        self._unsubscribe: Callable[[], None] | None = None
        self._mac_to_serial_map: dict[str, str] = {}
        self._is_running = False
        # Statistics tracking
        self._messages_received: int = 0
        self._messages_processed: int = 0
        self._last_message_time: datetime | None = None
        self._start_time: datetime | None = None

    @property
    def is_running(self) -> bool:
        """Return True if the MQTT service is running."""
        return self._is_running

    @property
    def messages_received(self) -> int:
        """Return total messages received."""
        return self._messages_received

    @property
    def messages_processed(self) -> int:
        """Return total messages successfully processed."""
        return self._messages_processed

    @property
    def last_message_time(self) -> datetime | None:
        """Return time of last received message."""
        return self._last_message_time

    @property
    def start_time(self) -> datetime | None:
        """Return service start time."""
        return self._start_time

    def get_statistics(self) -> dict:
        """Return MQTT service statistics."""
        return {
            "is_running": self._is_running,
            "messages_received": self._messages_received,
            "messages_processed": self._messages_processed,
            "last_message_time": (
                self._last_message_time.isoformat() if self._last_message_time else None
            ),
            "start_time": self._start_time.isoformat() if self._start_time else None,
            "sensors_mapped": len(self._mac_to_serial_map),
        }

    async def async_start(self) -> bool:
        """
        Start the MQTT service by subscribing to Meraki topics.

        Returns
        -------
            True if subscription was successful, False otherwise.

        """
        if self._is_running:
            _LOGGER.debug("MQTT service already running")
            return True

        # Build MAC to serial mapping from coordinator data
        self._build_mac_to_serial_map()

        try:
            # Subscribe to Meraki MT sensor topics
            self._unsubscribe = await mqtt.async_subscribe(
                self._hass,
                MERAKI_MQTT_MT_TOPIC_PATTERN,
                self._async_handle_message,
                qos=0,
            )
            self._is_running = True
            self._start_time = datetime.now()
            _LOGGER.info(
                "MQTT service started, subscribed to %s", MERAKI_MQTT_MT_TOPIC_PATTERN
            )
            return True
        except (TimeoutError, OSError, ValueError, AttributeError) as err:
            # TimeoutError: Connection timeout
            # OSError: Network/socket errors
            # ValueError: Invalid topic or configuration
            # AttributeError: MQTT integration not properly loaded
            _LOGGER.error("Failed to subscribe to MQTT topics: %s", err)
            return False

    async def async_stop(self) -> None:
        """Stop the MQTT service and unsubscribe from topics."""
        if self._unsubscribe is not None:
            self._unsubscribe()
            self._unsubscribe = None
        self._is_running = False
        _LOGGER.info("MQTT service stopped")

    def _build_mac_to_serial_map(self) -> None:
        """Build a mapping from sensor MAC addresses to device serials."""
        self._mac_to_serial_map.clear()

        if not self._coordinator.data:
            return

        devices = self._coordinator.data.get("devices", [])
        for device in devices:
            model = device.get("model", "")
            if model.startswith("MT"):
                # Meraki MT sensors have a 'mac' field
                mac = device.get("mac")
                serial = device.get("serial")
                if mac and serial:
                    # Normalize MAC address format (uppercase, colon-separated)
                    normalized_mac = normalize_mac(mac)
                    self._mac_to_serial_map[normalized_mac] = serial

        _LOGGER.debug(
            "Built MAC to serial map with %d MT sensors",
            len(self._mac_to_serial_map),
        )

    @callback
    def _async_handle_message(self, msg: mqtt.ReceiveMessage) -> None:
        """
        Handle incoming MQTT message.

        Args:
        ----
            msg: The received MQTT message.

        """
        self._messages_received += 1
        self._last_message_time = datetime.now()

        topic = msg.topic
        payload = msg.payload

        # Forward to relay manager if configured
        if self._relay_manager is not None:
            self._hass.async_create_task(
                self._relay_manager.async_relay_message(topic, payload)
            )

        # Parse the topic to extract components
        match = MERAKI_MT_TOPIC_REGEX.match(topic)
        if not match:
            _LOGGER.debug("Received message on non-MT topic: %s", topic)
            return

        network_id = match.group("network_id")
        sensor_mac = match.group("sensor_mac")
        metric = match.group("metric")

        # Normalize the MAC address (uses LRU cache for performance)
        normalized_mac = normalize_mac(sensor_mac)

        # Look up device serial from MAC
        serial = self._mac_to_serial_map.get(normalized_mac)
        if not serial:
            _LOGGER.debug(
                "Received MQTT data for unknown sensor MAC: %s (network: %s)",
                sensor_mac,
                network_id,
            )
            # Rebuild map in case new devices were added
            self._build_mac_to_serial_map()
            serial = self._mac_to_serial_map.get(normalized_mac)
            if not serial:
                return

        # Parse the payload
        try:
            if isinstance(payload, bytes):
                payload_str = payload.decode("utf-8")
            else:
                payload_str = str(payload)
            data = json.loads(payload_str)
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            _LOGGER.warning(
                "Failed to parse MQTT payload for %s/%s: %s",
                serial,
                metric,
                err,
            )
            return

        _LOGGER.debug(
            "Received MQTT update for sensor %s, metric %s: %s",
            serial,
            metric,
            data,
        )

        self._messages_processed += 1

        # Update the coordinator with the new data
        self._hass.async_create_task(
            self._coordinator.async_update_from_mqtt(serial, metric, data)
        )

    def update_mac_mapping(self) -> None:
        """Rebuild the MAC to serial mapping (call after coordinator refresh)."""
        self._build_mac_to_serial_map()
