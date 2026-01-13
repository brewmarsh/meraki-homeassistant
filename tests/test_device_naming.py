"""Tests for consistent device name formatting across various entity types."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANIDSensor
from custom_components.meraki_ha.sensor.org.org_clients import (
    MerakiOrganizationSSIDClientsSensor,
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
<<<<<<< HEAD
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
    """Fixture for a mocked MerakiDataCoordinator."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    """Fixture for a mocked MerakiDataCoordinator."""
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
                {"id": 1, "name": "Test VLAN", "enabled": True},
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
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("Org sensor device_info is None")
=======
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("Org sensor device_info is None")
=======
    assert device_info is not None
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    assert device_info is not None
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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

    network_data = {
        "id": network_id,
        "name": network_name,
        "productTypes": ["wireless"],
    }

    sensor = MerakiNetworkClientsSensor(
        mock_coordinator,
        mock_coordinator.config_entry,
        network_data,
        MagicMock(),
    )
    device_info = sensor.device_info
<<<<<<< HEAD
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("Network sensor device_info is None")
=======
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("Network sensor device_info is None")
=======
    assert device_info is not None
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    assert device_info is not None
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("VLAN sensor device_info is None")
=======
<<<<<<< HEAD
    if device_info is None:
        pytest.fail("VLAN sensor device_info is None")
=======
    assert device_info is not None
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    assert device_info is not None
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    assert device_info["name"] == "[VLAN] Test VLAN"
