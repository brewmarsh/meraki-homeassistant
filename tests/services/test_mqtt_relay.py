"""Tests for the MQTT Relay Manager."""

from unittest.mock import AsyncMock

import pytest

from custom_components.meraki_ha.services.mqtt_relay import (
    ConnectionStatus,
    MqttRelayDestination,
    MqttRelayManager,
    RelayDestinationConfig,
)


class TestRelayDestinationConfig:
    """Tests for RelayDestinationConfig."""

    def test_from_dict_minimal(self):
        """Test creating config from minimal dictionary."""
        data = {
            "name": "Test Destination",
            "host": "mqtt.example.com",
        }

        config = RelayDestinationConfig.from_dict(data)

        assert config.name == "Test Destination"
        assert config.host == "mqtt.example.com"
        assert config.port == 1883
        assert config.username is None
        assert config.password is None
        assert config.use_tls is False
        assert config.topic_filter == "meraki/v1/mt/#"
        assert config.device_types == []

    def test_from_dict_full(self):
        """Test creating config from full dictionary."""
        data = {
            "name": "IoT Platform",
            "host": "iot.example.com",
            "port": 8883,
            "username": "mqtt_user",
            "password": "mqtt_pass",
            "use_tls": True,
            "topic_filter": "meraki/v1/mt/+/ble/#",
            "device_types": ["MT10", "MT14"],
        }

        config = RelayDestinationConfig.from_dict(data)

        assert config.name == "IoT Platform"
        assert config.host == "iot.example.com"
        assert config.port == 8883
        assert config.username == "mqtt_user"
        assert config.password == "mqtt_pass"
        assert config.use_tls is True
        assert config.topic_filter == "meraki/v1/mt/+/ble/#"
        assert config.device_types == ["MT10", "MT14"]

    def test_from_dict_tls_default_port(self):
        """Test that TLS enabled uses default TLS port when port not specified."""
        data = {
            "name": "TLS Destination",
            "host": "secure.example.com",
            "use_tls": True,
        }

        config = RelayDestinationConfig.from_dict(data)

        assert config.port == 8883  # TLS default port

    def test_from_dict_port_float_to_int(self):
        """Test that port is converted from float to int.

        Home Assistant's NumberSelector returns float values (e.g., 1883.0),
        but aiomqtt expects int. This test ensures the conversion works.
        """
        data = {
            "name": "Float Port Test",
            "host": "mqtt.example.com",
            "port": 1883.0,  # Float as returned by HA NumberSelector
        }

        config = RelayDestinationConfig.from_dict(data)

        assert config.port == 1883
        assert isinstance(config.port, int)

    def test_from_dict_port_string_to_int(self):
        """Test that port handles string values gracefully."""
        data = {
            "name": "String Port Test",
            "host": "mqtt.example.com",
            "port": "8883",  # String value
        }

        config = RelayDestinationConfig.from_dict(data)

        assert config.port == 8883
        assert isinstance(config.port, int)


class TestMqttRelayDestination:
    """Tests for MqttRelayDestination."""

    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        return RelayDestinationConfig(
            name="Test Destination",
            host="mqtt.example.com",
            port=1883,
            topic_filter="meraki/v1/mt/#",
        )

    def test_matches_topic_wildcard_hash(self, config):
        """Test topic matching with # wildcard."""
        destination = MqttRelayDestination(config)

        # Should match
        assert destination.matches_topic(
            "meraki/v1/mt/N_123/ble/AA:BB:CC:DD:EE:FF/temperature"
        )
        assert destination.matches_topic(
            "meraki/v1/mt/L_456/ble/11:22:33:44:55:66/humidity"
        )

        # Should not match
        assert not destination.matches_topic("meraki/v1/camera/N_123/video")

    def test_matches_topic_wildcard_plus(self):
        """Test topic matching with + wildcard."""
        config = RelayDestinationConfig(
            name="Test",
            host="localhost",
            topic_filter="meraki/v1/mt/+/ble/+/temperature",
        )
        destination = MqttRelayDestination(config)

        # Should match temperature topics
        assert destination.matches_topic(
            "meraki/v1/mt/N_123/ble/AA:BB:CC:DD:EE:FF/temperature"
        )

        # Should not match humidity
        assert not destination.matches_topic(
            "meraki/v1/mt/N_123/ble/AA:BB:CC:DD:EE:FF/humidity"
        )

    def test_initial_status_disconnected(self, config):
        """Test that initial status is disconnected."""
        destination = MqttRelayDestination(config)
        assert destination.status == ConnectionStatus.DISCONNECTED

    def test_name_property(self, config):
        """Test name property returns correct value."""
        destination = MqttRelayDestination(config)
        assert destination.name == "Test Destination"

    @pytest.mark.asyncio
    async def test_async_publish_when_not_running(self, config):
        """Test that publishing when not running does nothing."""
        destination = MqttRelayDestination(config)

        # Should not raise, just silently ignore
        await destination.async_publish("test/topic", b"test payload")

    @pytest.mark.asyncio
    async def test_async_stop_when_not_started(self, config):
        """Test that stopping when not started is safe."""
        destination = MqttRelayDestination(config)

        # Should not raise
        await destination.async_stop()
        assert destination.status == ConnectionStatus.DISCONNECTED


class TestMqttRelayManager:
    """Tests for MqttRelayManager."""

    def test_empty_destinations(self):
        """Test manager with no destinations configured."""
        manager = MqttRelayManager([])

        assert len(manager.destinations) == 0

    def test_creates_destinations_from_config(self):
        """Test that destinations are created from config."""
        configs = [
            {"name": "Dest1", "host": "host1.example.com"},
            {"name": "Dest2", "host": "host2.example.com"},
        ]

        manager = MqttRelayManager(configs)

        assert len(manager.destinations) == 2
        assert manager.destinations[0].name == "Dest1"
        assert manager.destinations[1].name == "Dest2"

    def test_skips_destinations_without_host(self):
        """Test that destinations without host are skipped."""
        configs = [
            {"name": "Valid", "host": "host.example.com"},
            {"name": "Invalid", "host": ""},  # Empty host
        ]

        manager = MqttRelayManager(configs)

        assert len(manager.destinations) == 1
        assert manager.destinations[0].name == "Valid"

    def test_get_health_status(self):
        """Test getting health status for all destinations."""
        configs = [
            {"name": "Dest1", "host": "host1.example.com", "port": 1883},
            {
                "name": "Dest2",
                "host": "host2.example.com",
                "port": 8883,
                "use_tls": True,
            },
        ]

        manager = MqttRelayManager(configs)
        status = manager.get_health_status()

        assert "Dest1" in status
        assert status["Dest1"]["status"] == "disconnected"
        assert status["Dest1"]["host"] == "host1.example.com"
        assert status["Dest1"]["port"] == 1883

        assert "Dest2" in status
        assert status["Dest2"]["status"] == "disconnected"

    @pytest.mark.asyncio
    async def test_async_relay_message_to_matching_destinations(self):
        """Test that messages are relayed to matching destinations only."""
        configs = [
            {
                "name": "MT Only",
                "host": "mt.example.com",
                "topic_filter": "meraki/v1/mt/#",
            },
            {
                "name": "Camera Only",
                "host": "cam.example.com",
                "topic_filter": "meraki/v1/camera/#",
            },
        ]

        manager = MqttRelayManager(configs)

        # Mock the publish method on destinations
        for dest in manager.destinations:
            dest.async_publish = AsyncMock()

        # Relay an MT message
        await manager.async_relay_message(
            "meraki/v1/mt/N_123/ble/AA:BB:CC:DD:EE:FF/temperature", b'{"celsius": 22.5}'
        )

        # Only MT destination should receive it
        manager.destinations[0].async_publish.assert_called_once()
        manager.destinations[1].async_publish.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_start_starts_all_destinations(self):
        """Test that async_start starts all destinations."""
        configs = [
            {"name": "Dest1", "host": "host1.example.com"},
            {"name": "Dest2", "host": "host2.example.com"},
        ]

        manager = MqttRelayManager(configs)

        # Mock async_start on destinations
        for dest in manager.destinations:
            dest.async_start = AsyncMock()

        await manager.async_start()

        for dest in manager.destinations:
            dest.async_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_stop_stops_all_destinations(self):
        """Test that async_stop stops all destinations."""
        configs = [
            {"name": "Dest1", "host": "host1.example.com"},
            {"name": "Dest2", "host": "host2.example.com"},
        ]

        manager = MqttRelayManager(configs)

        # Mock async_stop on destinations
        for dest in manager.destinations:
            dest.async_stop = AsyncMock()

        await manager.async_stop()

        for dest in manager.destinations:
            dest.async_stop.assert_called_once()
