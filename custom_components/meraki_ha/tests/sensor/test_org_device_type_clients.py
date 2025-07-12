import pytest
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.meraki_ha.sensor.org_device_type_clients import MerakiOrgDeviceTypeClientsSensor
from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinators import MerakiDataUpdateCoordinator

ORGANIZATION_ID = "test_org_id"
ORGANIZATION_NAME = "Test Organization"

@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
    coordinator.data = {
        "clients_on_ssids": 10,
        "clients_on_appliances": 5,
        "clients_on_wireless": 12,
        "organization_info": {"name": ORGANIZATION_NAME}
    }
    coordinator.org_id = ORGANIZATION_ID
    coordinator.org_name = ORGANIZATION_NAME
    return coordinator

async def test_sensor_creation_and_initial_state(
    mock_coordinator: MagicMock
):
    """Test sensor creation and its initial state based on coordinator data."""

    sensor = MerakiOrgDeviceTypeClientsSensor(
        coordinator=mock_coordinator,
        organization_id=ORGANIZATION_ID,
        organization_name=ORGANIZATION_NAME
    )

    assert sensor.unique_id == f"meraki_org_{ORGANIZATION_ID}_client_types"
    assert sensor.name == f"{ORGANIZATION_NAME} Client Types"
    assert sensor.icon == "mdi:account-group"
    assert sensor.state_class == "measurement"
    assert sensor.native_unit_of_measurement == "clients"

    # Check initial native value (sum of counts)
    expected_total = mock_coordinator.data["clients_on_ssids"] + \
                     mock_coordinator.data["clients_on_appliances"] + \
                     mock_coordinator.data["clients_on_wireless"]
    assert sensor.native_value == expected_total

    # Check attributes
    expected_attributes = {
        "organization_id": ORGANIZATION_ID,
        "clients_on_ssids": mock_coordinator.data["clients_on_ssids"],
        "clients_on_appliances": mock_coordinator.data["clients_on_appliances"],
        "clients_on_wireless": mock_coordinator.data["clients_on_wireless"],
    }
    assert sensor.extra_state_attributes == expected_attributes

    # Device Info
    assert sensor.device_info is not None
    assert sensor.device_info["identifiers"] == {(DOMAIN, ORGANIZATION_ID)}
    assert sensor.device_info["name"] == f"Meraki Organization: {ORGANIZATION_NAME}"
    assert sensor.device_info["manufacturer"] == "Cisco Meraki"
    assert sensor.device_info["model"] == "Organization"


async def test_sensor_state_update_from_coordinator(
    mock_coordinator: MagicMock
):
    """Test sensor state updates when coordinator data changes."""
    sensor = MerakiOrgDeviceTypeClientsSensor(
        coordinator=mock_coordinator,
        organization_id=ORGANIZATION_ID,
        organization_name=ORGANIZATION_NAME
    )

    # Simulate coordinator update
    updated_data = {
        "clients_on_ssids": 15,
        "clients_on_appliances": 7,
        "clients_on_wireless": 20,
        "organization_info": {"name": ORGANIZATION_NAME}
    }
    mock_coordinator.data = updated_data

    # Manually trigger the update method that HA would call
    sensor._handle_coordinator_update()
    # Or directly sensor._update_sensor_state() if _handle_coordinator_update just calls that and async_write_ha_state

    expected_total_updated = updated_data["clients_on_ssids"] + \
                             updated_data["clients_on_appliances"] + \
                             updated_data["clients_on_wireless"]
    assert sensor.native_value == expected_total_updated

    expected_attributes_updated = {
        "organization_id": ORGANIZATION_ID,
        "clients_on_ssids": updated_data["clients_on_ssids"],
        "clients_on_appliances": updated_data["clients_on_appliances"],
        "clients_on_wireless": updated_data["clients_on_wireless"],
    }
    assert sensor.extra_state_attributes == expected_attributes_updated


async def test_sensor_missing_data_in_coordinator(
    mock_coordinator: MagicMock
):
    """Test sensor behavior when specific data is missing from coordinator."""
    mock_coordinator.data = {
        "organization_info": {"name": ORGANIZATION_NAME}
    }

    sensor = MerakiOrgDeviceTypeClientsSensor(
        coordinator=mock_coordinator,
        organization_id=ORGANIZATION_ID,
        organization_name=ORGANIZATION_NAME
    )

    assert sensor.native_value == 0
    expected_attributes_missing = {
        "organization_id": ORGANIZATION_ID,
        "clients_on_ssids": 0,
        "clients_on_appliances": 0,
        "clients_on_wireless": 0,
    }
    assert sensor.extra_state_attributes == expected_attributes_missing

async def test_sensor_coordinator_data_is_none(
    mock_coordinator: MagicMock
):
    """Test sensor behavior when coordinator.data is None."""
    mock_coordinator.data = None

    sensor = MerakiOrgDeviceTypeClientsSensor(
        coordinator=mock_coordinator,
        organization_id=ORGANIZATION_ID,
        organization_name=ORGANIZATION_NAME
    )

    assert sensor.native_value == 0
    expected_attributes_none = {
        "organization_id": ORGANIZATION_ID,
        "clients_on_ssids": 0,
        "clients_on_appliances": 0,
        "clients_on_wireless": 0,
    }
    assert sensor.extra_state_attributes == expected_attributes_none
