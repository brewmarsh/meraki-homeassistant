"""
MQTT Relay Manager for Meraki Integration.

This module handles relaying Meraki MQTT messages to external brokers.
Supports multiple destinations with topic filtering.
"""

from __future__ import annotations

import asyncio
import fnmatch
import logging
import ssl
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import aiomqtt

from ..const import (
    DEFAULT_MQTT_PORT,
    DEFAULT_MQTT_TLS_PORT,
    MQTT_DEST_DEVICE_TYPES,
    MQTT_DEST_HOST,
    MQTT_DEST_NAME,
    MQTT_DEST_PASSWORD,
    MQTT_DEST_PORT,
    MQTT_DEST_TOPIC_FILTER,
    MQTT_DEST_USE_TLS,
    MQTT_DEST_USERNAME,
)

_LOGGER = logging.getLogger(__name__)

# Connection retry settings
RETRY_INTERVAL_SECONDS = 30
MAX_RETRY_ATTEMPTS = 10


class ConnectionStatus(Enum):
    """Connection status for relay destinations."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class RelayDestinationConfig:
    """Configuration for a single relay destination."""

    name: str
    host: str
    port: int = DEFAULT_MQTT_PORT
    username: str | None = None
    password: str | None = None
    use_tls: bool = False
    topic_filter: str = "meraki/v1/mt/#"
    device_types: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RelayDestinationConfig:
        """Create a RelayDestinationConfig from a dictionary."""
        return cls(
            name=data.get(MQTT_DEST_NAME, "Unnamed"),
            host=data.get(MQTT_DEST_HOST, ""),
            port=data.get(
                MQTT_DEST_PORT,
                DEFAULT_MQTT_TLS_PORT
                if data.get(MQTT_DEST_USE_TLS)
                else DEFAULT_MQTT_PORT,
            ),
            username=data.get(MQTT_DEST_USERNAME),
            password=data.get(MQTT_DEST_PASSWORD),
            use_tls=data.get(MQTT_DEST_USE_TLS, False),
            topic_filter=data.get(MQTT_DEST_TOPIC_FILTER, "meraki/v1/mt/#"),
            device_types=data.get(MQTT_DEST_DEVICE_TYPES, []),
        )


class MqttRelayDestination:
    """
    Manages connection to a single external MQTT broker.

    Handles connection lifecycle, retry logic, and message publishing.
    """

    def __init__(self, config: RelayDestinationConfig) -> None:
        """
        Initialize the relay destination.

        Args:
        ----
            config: Configuration for this destination.

        """
        self._config = config
        self._client: aiomqtt.Client | None = None
        self._status = ConnectionStatus.DISCONNECTED
        self._retry_count = 0
        self._connect_task: asyncio.Task | None = None
        self._message_queue: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()
        self._publisher_task: asyncio.Task | None = None
        self._running = False
        # Statistics tracking
        self._messages_relayed: int = 0
        self._last_relay_time: datetime | None = None
        self._last_error: str | None = None
        self._last_error_time: datetime | None = None

    @property
    def name(self) -> str:
        """Return the destination name."""
        return self._config.name

    @property
    def status(self) -> ConnectionStatus:
        """Return the current connection status."""
        return self._status

    @property
    def config(self) -> RelayDestinationConfig:
        """Return the destination configuration."""
        return self._config

    @property
    def messages_relayed(self) -> int:
        """Return the total number of messages relayed."""
        return self._messages_relayed

    @property
    def last_relay_time(self) -> datetime | None:
        """Return the time of the last relayed message."""
        return self._last_relay_time

    @property
    def last_error(self) -> str | None:
        """Return the last error message."""
        return self._last_error

    @property
    def last_error_time(self) -> datetime | None:
        """Return the time of the last error."""
        return self._last_error_time

    def matches_topic(self, topic: str) -> bool:
        """
        Check if this destination should receive messages for the given topic.

        Args:
        ----
            topic: The MQTT topic to check.

        Returns
        -------
            True if this destination should receive the message.

        """
        # Convert MQTT wildcards to fnmatch patterns
        pattern = self._config.topic_filter.replace("+", "*").replace("#", "*")
        return fnmatch.fnmatch(topic, pattern)

    async def async_start(self) -> None:
        """Start the relay destination connection."""
        if self._running:
            return

        self._running = True
        self._publisher_task = asyncio.create_task(self._async_publisher_loop())
        _LOGGER.info(
            "Started relay destination '%s' -> %s:%d",
            self._config.name,
            self._config.host,
            self._config.port,
        )

    async def async_stop(self) -> None:
        """Stop the relay destination and disconnect."""
        self._running = False

        if self._publisher_task:
            self._publisher_task.cancel()
            try:
                await self._publisher_task
            except asyncio.CancelledError:
                pass
            self._publisher_task = None

        if self._client:
            try:
                await self._client.__aexit__(None, None, None)
            except Exception as err:
                _LOGGER.debug("Error disconnecting from %s: %s", self._config.name, err)
            self._client = None

        self._status = ConnectionStatus.DISCONNECTED
        _LOGGER.info("Stopped relay destination '%s'", self._config.name)

    async def async_publish(self, topic: str, payload: bytes | str) -> None:
        """
        Queue a message for publishing to this destination.

        Args:
        ----
            topic: The MQTT topic.
            payload: The message payload.

        """
        if not self._running:
            return

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        await self._message_queue.put((topic, payload))

    async def _async_publisher_loop(self) -> None:
        """Run the main loop for publishing messages."""
        while self._running:
            try:
                await self._async_connect()

                while self._running and self._client:
                    try:
                        # Wait for messages with timeout
                        topic, payload = await asyncio.wait_for(
                            self._message_queue.get(),
                            timeout=30.0,
                        )
                        await self._client.publish(topic, payload)
                        self._messages_relayed += 1
                        self._last_relay_time = datetime.now()
                        _LOGGER.debug(
                            "Relayed message to '%s': %s (total: %d)",
                            self._config.name,
                            topic,
                            self._messages_relayed,
                        )
                    except TimeoutError:
                        # Keep connection alive
                        continue
                    except aiomqtt.MqttError as err:
                        self._last_error = str(err)
                        self._last_error_time = datetime.now()
                        _LOGGER.warning(
                            "MQTT error publishing to '%s': %s",
                            self._config.name,
                            err,
                        )
                        self._status = ConnectionStatus.ERROR
                        break

            except asyncio.CancelledError:
                break
            except Exception as err:
                self._last_error = str(err)
                self._last_error_time = datetime.now()
                _LOGGER.error(
                    "Error in publisher loop for '%s': %s",
                    self._config.name,
                    err,
                )
                self._status = ConnectionStatus.ERROR
                if self._running:
                    await asyncio.sleep(RETRY_INTERVAL_SECONDS)

    async def _async_connect(self) -> None:
        """Establish connection to the MQTT broker."""
        if self._client and self._status == ConnectionStatus.CONNECTED:
            return

        self._status = ConnectionStatus.CONNECTING

        while self._running and self._retry_count < MAX_RETRY_ATTEMPTS:
            try:
                # Build TLS context if needed
                tls_context = None
                if self._config.use_tls:
                    tls_context = ssl.create_default_context()

                self._client = aiomqtt.Client(
                    hostname=self._config.host,
                    port=self._config.port,
                    username=self._config.username,
                    password=self._config.password,
                    tls_context=tls_context,
                )

                await self._client.__aenter__()
                self._status = ConnectionStatus.CONNECTED
                self._retry_count = 0
                _LOGGER.info(
                    "Connected to relay destination '%s' at %s:%d",
                    self._config.name,
                    self._config.host,
                    self._config.port,
                )
                return

            except Exception as err:
                self._retry_count += 1
                _LOGGER.warning(
                    "Failed to connect to '%s' (attempt %d/%d): %s",
                    self._config.name,
                    self._retry_count,
                    MAX_RETRY_ATTEMPTS,
                    err,
                )
                self._status = ConnectionStatus.ERROR
                if self._running and self._retry_count < MAX_RETRY_ATTEMPTS:
                    await asyncio.sleep(RETRY_INTERVAL_SECONDS)

        if self._retry_count >= MAX_RETRY_ATTEMPTS:
            _LOGGER.error(
                "Max retry attempts reached for '%s'. Giving up.",
                self._config.name,
            )


class MqttRelayManager:
    """
    Manages multiple MQTT relay destinations.

    Routes incoming messages to appropriate destinations based on
    topic patterns and device type filters.
    """

    def __init__(self, destinations_config: list[dict[str, Any]]) -> None:
        """
        Initialize the relay manager.

        Args:
        ----
            destinations_config: List of destination configuration dictionaries.

        """
        self._destinations: list[MqttRelayDestination] = []
        for config_dict in destinations_config:
            config = RelayDestinationConfig.from_dict(config_dict)
            if config.host:  # Only add if host is configured
                self._destinations.append(MqttRelayDestination(config))

    @property
    def destinations(self) -> list[MqttRelayDestination]:
        """Return all configured destinations."""
        return self._destinations

    def get_health_status(self) -> dict[str, dict[str, Any]]:
        """
        Get health status for all destinations.

        Returns
        -------
            Dictionary mapping destination names to their status info.

        """
        return {
            dest.name: {
                "status": dest.status.value,
                "host": dest.config.host,
                "port": dest.config.port,
                "topic_filter": dest.config.topic_filter,
                "messages_relayed": dest.messages_relayed,
                "last_relay_time": (
                    dest.last_relay_time.isoformat() if dest.last_relay_time else None
                ),
                "last_error": dest.last_error,
                "last_error_time": (
                    dest.last_error_time.isoformat() if dest.last_error_time else None
                ),
            }
            for dest in self._destinations
        }

    async def async_start(self) -> None:
        """Start all relay destinations."""
        for destination in self._destinations:
            await destination.async_start()
        _LOGGER.info(
            "MQTT relay manager started with %d destinations", len(self._destinations)
        )

    async def async_stop(self) -> None:
        """Stop all relay destinations."""
        for destination in self._destinations:
            await destination.async_stop()
        _LOGGER.info("MQTT relay manager stopped")

    async def async_relay_message(self, topic: str, payload: bytes | str) -> None:
        """
        Relay a message to all matching destinations.

        Args:
        ----
            topic: The MQTT topic.
            payload: The message payload.

        """
        for destination in self._destinations:
            if destination.matches_topic(topic):
                await destination.async_publish(topic, payload)
