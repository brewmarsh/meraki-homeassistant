import pytest
from unittest.mock import MagicMock, patch

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceRegistry

from custom_components.meraki_ha.const import DOMAIN, ATTR_SSIDS
from custom_components.meraki_ha.sensor import (
    MerakiSSIDAvailabilitySensor,
)  # Assuming this is the correct sensor
from custom_components.meraki_ha.entity import (
    MerakiEntity,
)  # Base entity if needed for context

# Mock data for an AP device
AP_DEVICE_INFO_RAW = {
    "serial": "Q2AB-CDEF-GHIJ",
    "networkId": "N_12345",
    "model": "MR42",
    "name": "My AP",
    "tags": ["office"],
    # other fields as necessary for MerakiEntity or the sensor itself
}

# Mock data for an SSID on that AP's network
SSID_INFO_RAW = {
    "number": 0,
    "name": "My Office SSID",
    "enabled": True,
    "networkId": "N_12345",  # Ensure this matches the AP's networkId
    "status": "online",  # Assuming status is pre-calculated by DataAggregator
    # other fields as necessary
}


@pytest.fixture
def mock_config_entry():
    """Mock ConfigEntry instance."""
    return MagicMock(spec=ConfigEntry)


@pytest.fixture
def mock_coordinator(mock_config_entry):
    """Mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.config_entry = mock_config_entry
    coordinator.data = {
        "devices": [AP_DEVICE_INFO_RAW],
        "ssids": [SSID_INFO_RAW],
    }
    return coordinator


@pytest.fixture
def mock_device_registry():
    """Mock DeviceRegistry."""
    registry = MagicMock(spec=DeviceRegistry)

    def get_or_create(*, config_entry_id, identifiers, via_device=None, **kwargs):
        mock_device_entry = MagicMock()
        mock_device_entry.id = f"device_{list(identifiers)[0][1]}"
        if via_device:
            mock_device_entry.via_device_id = f"device_{list(via_device)[0][1]}"
        return mock_device_entry

    registry.async_get_or_create = MagicMock(side_effect=get_or_create)
    return registry


# Test function
def test_ssid_sensor_device_info_linking(
    mock_coordinator, mock_device_registry
):
    """Test that SSID-specific sensors correctly link their DeviceInfo to the parent AP device."""

    with patch(
        "homeassistant.helpers.device_registry.async_get",
        return_value=mock_device_registry,
    ):

        # Instantiate the sensor
        # We pass AP_DEVICE_INFO_RAW as `device_info_data` and SSID_INFO_RAW as `entity_specific_data`
        # This matches the expected signature for entity creation from a coordinator.
        # The actual MerakiEntity might process these differently.
        # The key is that the sensor's constructor receives enough info to build its DeviceInfo.

        # To accurately test MerakiSSIDAvailabilitySensor, we need to ensure its `_device_info_data`
        # and `_entity_specific_data` are set as they would be by the coordinator/platform.
        # The `MerakiEntity` constructor takes `coordinator`, `device_info_data`, `entity_specific_data`.

        sensor = MerakiSSIDAvailabilitySensor(
            coordinator=mock_coordinator,
            device_info_data=AP_DEVICE_INFO_RAW,  # This is the PARENT AP device
            entity_specific_data=SSID_INFO_RAW,  # This is the SSID itself
        )

        # Access the sensor's device_info property
        device_info = sensor.device_info

        assert device_info is not None

        # Assert that device_info.identifiers is correctly formed for the SSID entity
        # It should be unique for the SSID, typically combining networkId and SSID number (or serial if SSIDs were devices)
        # Based on current patterns, SSID entities are often namespaced under their network or AP.
        # If SSIDs are treated as "devices" themselves:
        expected_ssid_device_identifiers = {
            (DOMAIN, f"{SSID_INFO_RAW['networkId']}_{SSID_INFO_RAW['number']}")
        }
        assert device_info.identifiers == expected_ssid_device_identifiers

        # Assert that device_info.via_device links to the AP's identifiers
        # The AP's unique identifier is its serial number.
        expected_ap_device_identifiers = (DOMAIN, AP_DEVICE_INFO_RAW["serial"])
        assert device_info.via_device == expected_ap_device_identifiers

        mock_device_registry.async_get_or_create.assert_any_call(
            config_entry_id=mock_coordinator.config_entry.entry_id,
            identifiers=expected_ssid_device_identifiers,
            name=f"{AP_DEVICE_INFO_RAW['name']} SSID: {SSID_INFO_RAW['name']}",
            model=f"SSID ({AP_DEVICE_INFO_RAW['model']})",
            manufacturer="Cisco Meraki",
            via_device=expected_ap_device_identifiers,
        )


# Placeholder test to make sure pytest picks up the file
def test_placeholder_sensor():
    assert True
