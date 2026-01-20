
"""Tests for the Meraki network clients sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.types import MerakiNetwork
from tests.const import MOCK_NETWORK


async def test_network_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki network clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {}  # Data is no longer read from coordinator
    config_entry = MagicMock()
    sensor = MerakiNetworkClientsSensor(
        coordinator, config_entry, MOCK_NETWORK, MagicMock()
    )
    sensor._update_sensor_data()
    assert sensor.native_value == 0
