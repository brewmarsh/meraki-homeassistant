"""Tests for consistent device name formatting across various entity types."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

<<<<<<< HEAD
=======
from custom_components.meraki_ha.core.utils.naming_utils import format_device_name
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANIDSensor
from custom_components.meraki_ha.sensor.org.org_clients import (
    MerakiOrganizationSSIDClientsSensor,
)
<<<<<<< HEAD
=======
from custom_components.meraki_ha.types import MerakiVlan
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


@pytest.fixture
def mock_coordinator() -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataCoordinator."""
=======
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "networks": [
            {
                "id": "net1",
                "name": "Test Network",
                "productTypes": ["appliance", "switch", "wireless"],
            },
        ],
        "vlans": {
            "net1": [
<<<<<<< HEAD
                {"id": 1, "name": "Test VLAN", "enabled": True},
=======
                MerakiVlan(id=1, name="Test VLAN"),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            ],
        },
    }
    return coordinator


def test_org_device_naming(mock_coordinator: MagicMock) -> None:
    """
    Test name formatting for an organization-level device.

    Args:
    ----
        mock_coordinator: The mocked coordinator.

    """
    org_id = "org1"
    org_name = "Test Organization"

    sensor = MerakiOrganizationSSIDClientsSensor(mock_coordinator, org_id, org_name)
    device_info = sensor.device_info
<<<<<<< HEAD
    assert device_info is not None
=======
    if device_info is None:
        pytest.fail("Org sensor device_info is None")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    assert device_info["name"] == "[Organization] Test Organization"


def test_network_device_naming(mock_coordinator: MagicMock) -> None:
    """
    Test name formatting for a network-level device.

    Args:
    ----
        mock_coordinator: The mocked coordinator.

    """
    network_id = "net1"
    network_name = "Test Network"

<<<<<<< HEAD
    network_data = {
        "id": network_id,
        "name": network_name,
        "productTypes": ["wireless"],
    }
=======
    from custom_components.meraki_ha.types import MerakiNetwork

    network_data = MerakiNetwork(
        id=network_id,
        name=network_name,
        product_types=["wireless"],
        organization_id="org1",
    )
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    sensor = MerakiNetworkClientsSensor(
        mock_coordinator,
        mock_coordinator.config_entry,
        network_data,
        MagicMock(),
    )
    device_info = sensor.device_info
<<<<<<< HEAD
    assert device_info is not None
=======
    if device_info is None:
        pytest.fail("Network sensor device_info is None")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    assert device_info["name"] == "[Network] Test Network"


def test_vlan_device_naming(mock_coordinator: MagicMock) -> None:
    """
    Test name formatting for a VLAN-level device.

    Args:
    ----
        mock_coordinator: The mocked coordinator.

    """
    network_id = "net1"
    vlan_data = mock_coordinator.data["vlans"]["net1"][0]

    sensor = MerakiVLANIDSensor(
        mock_coordinator,
        mock_coordinator.config_entry,
        network_id,
        vlan_data,
    )
    device_info = sensor.device_info
<<<<<<< HEAD
    assert device_info is not None
    assert device_info["name"] == "[VLAN] Test VLAN"
=======
    if device_info is None:
        pytest.fail("VLAN sensor device_info is None")
    assert device_info["name"] == "[VLAN] Test VLAN"


def test_camera_device_naming():
    """Test that camera devices are correctly prefixed."""
    camera_device = {
        "name": "Test Camera",
        "model": "MV12",
        "serial": "Q234-ABCD-5678",
    }
    config = {}
    formatted_name = format_device_name(camera_device, config)
    assert formatted_name == "[Camera] Test Camera"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
