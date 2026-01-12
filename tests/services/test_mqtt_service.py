"""Tests for the MerakiMqttService."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.services.mqtt_service import (
    MERAKI_MT_TOPIC_REGEX,
    MerakiMqttService,
    normalize_mac,
)


@pytest.fixture
def mock_hass():
    """Fixture for a mock Home Assistant instance."""
    hass = MagicMock()
    hass.async_create_task = MagicMock()
    return hass


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "mac": "54:6C:0E:8A:9E:81",
                "model": "MT10",
                "name": "Test MT10 Sensor",
            }
        ]
    }
    coordinator.async_update_from_mqtt = AsyncMock()
    return coordinator


@pytest.fixture
def mock_relay_manager():
    """Fixture for a mock MqttRelayManager."""
    manager = MagicMock()
    manager.async_relay_message = AsyncMock()
    return manager


class TestMqttTopicRegex:
    """Tests for the MQTT topic regex."""

    def test_valid_mt_topic(self):
        """Test parsing a valid MT sensor topic."""
        topic = "meraki/v1/mt/L_643451796760561416/ble/54:6C:0E:8A:9E:81/temperature"
        match = MERAKI_MT_TOPIC_REGEX.match(topic)

        assert match is not None
        assert match.group("network_id") == "L_643451796760561416"
        assert match.group("sensor_mac") == "54:6C:0E:8A:9E:81"
        assert match.group("metric") == "temperature"

    def test_humidity_topic(self):
        """Test parsing a humidity topic."""
        topic = "meraki/v1/mt/N_12345/ble/AA:BB:CC:DD:EE:FF/humidity"
        match = MERAKI_MT_TOPIC_REGEX.match(topic)

        assert match is not None
        assert match.group("metric") == "humidity"

    def test_battery_topic(self):
        """Test parsing a battery percentage topic."""
        topic = "meraki/v1/mt/L_test/ble/11:22:33:44:55:66/batteryPercentage"
        match = MERAKI_MT_TOPIC_REGEX.match(topic)

        assert match is not None
        assert match.group("metric") == "batteryPercentage"

    def test_invalid_topic(self):
        """Test that non-MT topics don't match."""
        topic = "meraki/v1/camera/N_123/video"
        match = MERAKI_MT_TOPIC_REGEX.match(topic)

        assert match is None

    def test_incomplete_topic(self):
        """Test that incomplete topics don't match."""
        topic = "meraki/v1/mt/L_123"
        match = MERAKI_MT_TOPIC_REGEX.match(topic)

        assert match is None


class TestMerakiMqttService:
    """Tests for the MerakiMqttService class."""

    def test_normalize_mac_with_colons(self):
        """Test MAC normalization with colon separators."""
        result = normalize_mac("54:6c:0e:8a:9e:81")
        assert result == "54:6C:0E:8A:9E:81"

    def test_normalize_mac_with_dashes(self):
        """Test MAC normalization with dash separators."""
        result = normalize_mac("54-6c-0e-8a-9e-81")
        assert result == "54:6C:0E:8A:9E:81"

    def test_normalize_mac_no_separators(self):
        """Test MAC normalization without separators."""
        result = normalize_mac("546c0e8a9e81")
        assert result == "54:6C:0E:8A:9E:81"

    def test_normalize_mac_uppercase(self):
        """Test MAC normalization for uppercase input."""
        result = normalize_mac("54:6C:0E:8A:9E:81")
        assert result == "54:6C:0E:8A:9E:81"

    def test_is_running_initially_false(self, mock_hass, mock_coordinator):
        """Test that is_running is False initially."""
        service = MerakiMqttService(mock_hass, mock_coordinator)
        assert service.is_running is False

    @pytest.mark.asyncio
    async def test_async_start_subscribes_to_mqtt(self, mock_hass, mock_coordinator):
        """Test that async_start subscribes to MQTT topics."""
        service = MerakiMqttService(mock_hass, mock_coordinator)

        with patch(
            "custom_components.meraki_ha.services.mqtt_service.mqtt.async_subscribe",
            new_callable=AsyncMock,
        ) as mock_subscribe:
            mock_subscribe.return_value = MagicMock()
            result = await service.async_start()

            assert result is True
            assert service.is_running is True
            mock_subscribe.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_start_failure_returns_false(self, mock_hass, mock_coordinator):
        """Test that async_start returns False on subscription failure."""
        service = MerakiMqttService(mock_hass, mock_coordinator)

        with patch(
            "custom_components.meraki_ha.services.mqtt_service.mqtt.async_subscribe",
            new_callable=AsyncMock,
            side_effect=OSError("MQTT not available"),
        ):
            result = await service.async_start()

            assert result is False
            assert service.is_running is False

    @pytest.mark.asyncio
    async def test_async_stop_unsubscribes(self, mock_hass, mock_coordinator):
        """Test that async_stop unsubscribes from MQTT."""
        service = MerakiMqttService(mock_hass, mock_coordinator)
        mock_unsubscribe = MagicMock()

        with patch(
            "custom_components.meraki_ha.services.mqtt_service.mqtt.async_subscribe",
            new_callable=AsyncMock,
            return_value=mock_unsubscribe,
        ):
            await service.async_start()
            await service.async_stop()

            mock_unsubscribe.assert_called_once()
            assert service.is_running is False

    def test_build_mac_to_serial_map(self, mock_hass, mock_coordinator):
        """Test building the MAC to serial mapping."""
        service = MerakiMqttService(mock_hass, mock_coordinator)
        service._build_mac_to_serial_map()

        assert "54:6C:0E:8A:9E:81" in service._mac_to_serial_map
        assert service._mac_to_serial_map["54:6C:0E:8A:9E:81"] == "Q234-ABCD-5678"

    def test_build_mac_to_serial_map_ignores_non_mt(self, mock_hass):
        """Test that non-MT devices are not included in the mapping."""
        coordinator = MagicMock()
        coordinator.data = {
            "devices": [
                {
                    "serial": "Q234-ABCD-5678",
                    "mac": "54:6C:0E:8A:9E:81",
                    "model": "MR46",  # Not an MT device
                    "name": "Test AP",
                }
            ]
        }

        service = MerakiMqttService(mock_hass, coordinator)
        service._build_mac_to_serial_map()

        assert len(service._mac_to_serial_map) == 0

    def test_update_mac_mapping(self, mock_hass, mock_coordinator):
        """Test that update_mac_mapping rebuilds the map."""
        service = MerakiMqttService(mock_hass, mock_coordinator)

        # Initially empty
        assert len(service._mac_to_serial_map) == 0

        # Call update
        service.update_mac_mapping()

        # Now populated
        assert len(service._mac_to_serial_map) == 1
