"""Tests for the appliance data parser."""

import logging

from custom_components.meraki_ha.core.parsers.appliance import (  # noqa: E402
    parse_appliance_data,
)
from custom_components.meraki_ha.types import MerakiDevice  # noqa: E402


def test_parse_appliance_data_success(caplog):
    """Test successful parsing of appliance uplink data."""
    caplog.set_level(logging.DEBUG)

    devices = [
        MerakiDevice(serial="MX75-1", name="MX75 Appliance"),
        MerakiDevice(serial="MS120-1", name="MS120 Switch"),
    ]

    appliance_uplink_statuses = [
        {
            "serial": "MX75-1",
            "uplinks": [
                {"interface": "wan1", "status": "active"},
                {"interface": "wan2", "status": "ready"},
            ],
        }
    ]

    parse_appliance_data(
        devices, {"appliance_uplink_statuses": appliance_uplink_statuses}
    )

    # Verify the MX75 was updated
    assert devices[0].serial == "MX75-1"
    assert len(devices[0].appliance_uplink_statuses) == 2
    assert devices[0].appliance_uplink_statuses[0]["interface"] == "wan1"

    # Verify the MS120 was not updated (no matching status)
    assert devices[1].serial == "MS120-1"
    assert len(devices[1].appliance_uplink_statuses) == 0

    # Verify logging
    assert "Parsing appliance data for 1 items" in caplog.text
    assert "Matched uplink data for MX75-1" in caplog.text


def test_parse_appliance_data_no_serial(caplog):
    """Test parsing when status data is missing a serial."""
    caplog.set_level(logging.DEBUG)

    devices = [MerakiDevice(serial="MX75-1")]
    appliance_uplink_statuses = [{"uplinks": []}]  # No serial

    parse_appliance_data(
        devices, {"appliance_uplink_statuses": appliance_uplink_statuses}
    )

    assert len(devices[0].appliance_uplink_statuses) == 0
    assert "Parsing appliance data for 1 items" in caplog.text
    assert "Matched uplink data" not in caplog.text


def test_parse_appliance_data_no_match(caplog):
    """Test parsing when no devices match the status serial."""
    caplog.set_level(logging.DEBUG)

    devices = [MerakiDevice(serial="OTHER-SERIAL")]
    appliance_uplink_statuses = [
        {"serial": "MX75-1", "uplinks": [{"interface": "wan1"}]}
    ]

    parse_appliance_data(
        devices, {"appliance_uplink_statuses": appliance_uplink_statuses}
    )

    assert len(devices[0].appliance_uplink_statuses) == 0
    assert "Parsing appliance data for 1 items" in caplog.text
    assert "Matched uplink data for MX75-1" not in caplog.text


def test_parse_appliance_data_exception(caplog):
    """Test parsing when appliance_uplink_statuses is an Exception."""
    devices = [MerakiDevice(serial="MX75-1")]
    appliance_uplink_statuses = Exception("API Error")

    parse_appliance_data(
        devices, {"appliance_uplink_statuses": appliance_uplink_statuses}
    )

    assert len(devices[0].appliance_uplink_statuses) == 0
    assert "Could not fetch appliance uplink statuses" in caplog.text


def test_parse_appliance_data_fallback(caplog):
    """Test parsing with fallback to previous_data."""
    caplog.set_level(logging.DEBUG)

    devices = [MerakiDevice(serial="MX75-1")]
    previous_data = {
        "appliance_uplink_statuses": [
            {
                "serial": "MX75-1",
                "uplinks": [{"interface": "wan1", "status": "active"}],
            }
        ]
    }

    # Pass empty detail_data
    parse_appliance_data(devices, {}, previous_data)

    assert len(devices[0].appliance_uplink_statuses) == 1
    assert devices[0].appliance_uplink_statuses[0]["interface"] == "wan1"
    assert "Matched uplink data for MX75-1" in caplog.text


def test_parse_appliance_data_with_ports():
    """Test parsing of appliance port data via parse_appliance_data."""
    devices = [
        MerakiDevice(serial="MX67-1", network_id="N_1"),
    ]

    detail_data = {
        "appliance_uplink_statuses": [{"serial": "MX67-1", "uplinks": []}],
        "appliance_ports_N_1": [
            {"number": 1, "enabled": True, "status": "Connected"},
            {"number": 2, "enabled": False, "status": "Disconnected"},
        ],
    }

    parse_appliance_data(devices, detail_data)

    assert len(devices[0].appliance_ports) == 2
    assert devices[0].appliance_ports[0].number == 1
    assert devices[0].appliance_ports[0].enabled is True
    assert devices[0].appliance_ports[0].status == "Connected"
    assert devices[0].appliance_ports[1].number == 2
    assert devices[0].appliance_ports[1].enabled is False
    assert devices[0].appliance_ports[1].status == "Disconnected"
