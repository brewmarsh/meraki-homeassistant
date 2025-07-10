import pytest
from unittest.mock import MagicMock, patch
import asyncio

from custom_components.meraki_ha.coordinators.data_aggregator import DataAggregator
from custom_components.meraki_ha.helpers.ssid_status_calculator import (
    SsidStatusCalculator,
)

# Mock raw data inputs - simplified to match current DataAggregator.aggregate_data inputs
PROCESSED_DEVICES_MR = [
    {
        "serial": "MR1",
        "model": "MR52",
        "networkId": "N1",
        "tags": ["tag1"],
        "name": "AP1",
    },
    {
        "serial": "MR2",
        "model": "MR42",
        "networkId": "N1",
        "tags": ["tag2"],
        "name": "AP2",
    },
]
PROCESSED_DEVICES_MS = [
    {"serial": "MS1", "model": "MS220", "networkId": "N1", "name": "Switch1"}
]
PROCESSED_DEVICES_MX = [
    {"serial": "MX1", "model": "MX64", "networkId": "N1", "name": "Firewall1"}
]
ALL_PROCESSED_DEVICES = (
    PROCESSED_DEVICES_MR + PROCESSED_DEVICES_MS + PROCESSED_DEVICES_MX
)

SSID_DATA_N1 = [
    {"number": 0, "name": "SSID1-N1", "networkId": "N1", "enabled": True},
    {"number": 1, "name": "SSID2-N1", "networkId": "N1", "enabled": False},
]
SSID_DATA_N2 = [  # Example for another network, though not directly used by MRs in N1
    {"number": 0, "name": "SSID1-N2", "networkId": "N2", "enabled": True},
]
ALL_SSID_DATA = SSID_DATA_N1 + SSID_DATA_N2

NETWORK_DATA = [
    {"id": "N1", "name": "Network 1", "organizationId": "O1"},
    {"id": "N2", "name": "Network 2", "organizationId": "O1"},
]

CLIENT_DATA_N1 = [
    {
        "id": "C1",
        "mac": "00:11:22:01",
        "description": "Client 1",
        "networkId": "N1",
        "deviceSerial": "MR1",
    },
    {
        "id": "C2",
        "mac": "00:11:22:02",
        "description": "Client 2",
        "networkId": "N1",
        "deviceSerial": "MR1",
    },
]
ALL_CLIENT_DATA = CLIENT_DATA_N1  # Assuming client_data is a flat list

NETWORK_CLIENT_COUNTS = {"N1": 2, "N2": 0}


@pytest.fixture
def mock_data_processor():
    return MagicMock()


@pytest.fixture
def mock_ssid_status_calculator():
    # Mock the SsidStatusCalculator.calculate_ssid_status static method
    # to return SSIDs with a mock 'status' field.
    def mock_calculate_status(ssids, devices, relaxed_tag_match):
        ssids_with_status = []
        for ssid in ssids:
            ssid_copy = ssid.copy()
            # Simple mock status based on enabled state for testing
            ssid_copy["status"] = "online" if ssid_copy["enabled"] else "offline"
            ssids_with_status.append(ssid_copy)
        return ssids_with_status

    with patch.object(
        SsidStatusCalculator, "calculate_ssid_status", side_effect=mock_calculate_status
    ) as mock_calc:
        yield mock_calc


@pytest.fixture
def aggregator(
    mock_ssid_status_calculator_unused, # Renamed, as data_processor is removed
):
    # mock_ssid_status_calculator_unused ensures SsidStatusCalculator.calculate_ssid_status is patched
    return DataAggregator(
        relaxed_tag_match=False,
        # data_processor=mock_data_processor, # Removed
        ssid_status_calculator=MagicMock(
            spec=SsidStatusCalculator
        ),
    )


@pytest.mark.asyncio
async def test_successful_aggregation(aggregator, mock_ssid_status_calculator):
    # Call the method under test
    aggregated_data = await aggregator.aggregate_data(
        processed_devices=ALL_PROCESSED_DEVICES,
        ssid_data=ALL_SSID_DATA,
        network_data=NETWORK_DATA,
        client_data=ALL_CLIENT_DATA,
        network_client_counts=NETWORK_CLIENT_COUNTS,
    )

    # Assert top-level keys
    assert "devices" in aggregated_data
    assert "ssids" in aggregated_data
    assert "networks" in aggregated_data
    assert "clients" in aggregated_data
    assert "network_client_counts" in aggregated_data

    # Assert devices structure and SSID embedding for MR devices
    assert len(aggregated_data["devices"]) == len(ALL_PROCESSED_DEVICES)
    mr1_aggregated = next(d for d in aggregated_data["devices"] if d["serial"] == "MR1")
    mr2_aggregated = next(d for d in aggregated_data["devices"] if d["serial"] == "MR2")
    ms1_aggregated = next(d for d in aggregated_data["devices"] if d["serial"] == "MS1")

    assert "ssids" in mr1_aggregated
    assert len(mr1_aggregated["ssids"]) == len(
        SSID_DATA_N1
    )  # MR1 is in N1, should get all N1 SSIDs
    # Check if SSID data within the device matches the (mocked) status-enhanced SSIDs for that network
    for ssid_in_device in mr1_aggregated["ssids"]:
        original_ssid = next(
            s
            for s in SSID_DATA_N1
            if s["number"] == ssid_in_device["number"] and s["networkId"] == "N1"
        )
        assert ssid_in_device["name"] == original_ssid["name"]
        assert ssid_in_device["status"] == (
            "online" if original_ssid["enabled"] else "offline"
        )

    assert "ssids" in mr2_aggregated  # MR2 is also in N1
    assert len(mr2_aggregated["ssids"]) == len(SSID_DATA_N1)

    assert "ssids" not in ms1_aggregated  # MS device should not have SSIDs embedded

    # Assert SSIDs list (should be status-enhanced)
    assert len(aggregated_data["ssids"]) == len(ALL_SSID_DATA)
    for ssid in aggregated_data["ssids"]:
        assert "status" in ssid  # Mocked by mock_ssid_status_calculator
        original_ssid = next(
            s
            for s in ALL_SSID_DATA
            if s["number"] == ssid["number"] and s["networkId"] == ssid["networkId"]
        )
        assert ssid["status"] == ("online" if original_ssid["enabled"] else "offline")

    # Assert clients list (should be the same as input for now)
    assert aggregated_data["clients"] == ALL_CLIENT_DATA
    assert len(aggregated_data["clients"]) == len(ALL_CLIENT_DATA)

    # Assert networks list
    assert aggregated_data["networks"] == NETWORK_DATA
    assert len(aggregated_data["networks"]) == len(NETWORK_DATA)

    # Assert network client counts
    assert aggregated_data["network_client_counts"] == NETWORK_CLIENT_COUNTS

    # Ensure SsidStatusCalculator.calculate_ssid_status was called
    mock_ssid_status_calculator.assert_called_once_with(
        ssids=ALL_SSID_DATA, devices=ALL_PROCESSED_DEVICES, relaxed_tag_match=False
    )


# Minimal test to ensure the file is picked up by pytest
def test_placeholder():
    assert True


# Example of how you might test device_details merging if DataAggregator handled it:
# (This is NOT testing current DataAggregator behavior, but for future reference)
#
# RAW_DEVICES_FOR_MERGE = [
#     {"serial": "MR1", "model": "MR52", "networkId": "N1", "tags": ["tag1"], "name": "AP1_raw"},
#     {"serial": "MS1", "model": "MS220", "networkId": "N1", "name": "Switch1_raw"},
# ]
# DEVICE_DETAILS_FOR_MERGE = {
#     "MR1": {"lanIp": "192.168.1.1", "firmware": "MR 29.6.1", "connected_clients_count": 5},
#     "MS1": {"status": "online", "usingDhcp": True}
# }
#
# @pytest.mark.skip(reason="DataAggregator does not currently merge device_details this way")
# async def test_device_details_merging(aggregator):
#     # Assume aggregator's aggregate_data was modified to take raw_devices and device_details
#     # and perform merging. This is a hypothetical test.
#
#     # Patched aggregate_data might look like:
#     # def aggregate_data(self, raw_devices, device_details, ...):
#     #     processed_devices = []
#     #     for dev in raw_devices:
#     #         dev_copy = dev.copy()
#     #         if dev['serial'] in device_details:
#     #             dev_copy.update(device_details[dev['serial']])
#     #         processed_devices.append(dev_copy)
#     #     # ... rest of current aggregation logic ...
#     #     return {"devices": processed_devices, ...}
#
#     # This test would need DataAggregator to be re-written or this logic placed elsewhere.
#     # For now, this is a conceptual placeholder.
#
#     # Example call (hypothetical)
#     # aggregated_data = await aggregator.aggregate_data(
#     #     raw_devices=RAW_DEVICES_FOR_MERGE,
#     #     device_details=DEVICE_DETAILS_FOR_MERGE,
#     #     ssid_data=[], network_data=[], client_data=[], network_client_counts={}
#     # )
#     #
#     # mr1_merged = next(d for d in aggregated_data["devices"] if d["serial"] == "MR1")
#     # assert mr1_merged["name"] == "AP1_raw" # Original data
#     # assert mr1_merged["lanIp"] == "192.168.1.1" # Merged detail
#     # assert mr1_merged["connected_clients_count"] == 5 # Merged detail
#     pass

@pytest.mark.asyncio
async def test_aggregation_with_empty_inputs(aggregator, mock_ssid_status_calculator):
    """Test aggregation with empty lists for devices, SSIDs, and networks."""
    aggregated_data = await aggregator.aggregate_data(
        processed_devices=[],
        ssid_data=[],
        network_data=[],
        client_data=[],
        network_client_counts={},
        clients_on_ssids=0,
        clients_on_appliances=0,
        clients_on_wireless=0
    )

    assert aggregated_data["devices"] == []
    assert aggregated_data["ssids"] == [] # SsidStatusCalculator will be called with empty list
    assert aggregated_data["networks"] == []
    assert aggregated_data["clients"] == []
    assert aggregated_data["network_client_counts"] == {}
    assert aggregated_data["clients_on_ssids"] == 0
    assert aggregated_data["clients_on_appliances"] == 0
    assert aggregated_data["clients_on_wireless"] == 0

    mock_ssid_status_calculator.assert_called_once_with(
        ssids=[], devices=[], relaxed_tag_match=False
    )

@pytest.mark.asyncio
async def test_aggregation_with_none_client_data(aggregator, mock_ssid_status_calculator):
    """Test aggregation when optional client_data and network_client_counts are None."""
    aggregated_data = await aggregator.aggregate_data(
        processed_devices=ALL_PROCESSED_DEVICES, # Use some devices for SSID linking part
        ssid_data=ALL_SSID_DATA,
        network_data=NETWORK_DATA,
        client_data=None, # Test None case
        network_client_counts=None, # Test None case
        clients_on_ssids=10, # Arbitrary values
        clients_on_appliances=5,
        clients_on_wireless=8
    )

    assert len(aggregated_data["devices"]) == len(ALL_PROCESSED_DEVICES)
    assert len(aggregated_data["ssids"]) == len(ALL_SSID_DATA)
    assert aggregated_data["networks"] == NETWORK_DATA

    assert aggregated_data["clients"] == [] # Should default to empty list
    assert aggregated_data["network_client_counts"] == {} # Should default to empty dict

    assert aggregated_data["clients_on_ssids"] == 10
    assert aggregated_data["clients_on_appliances"] == 5
    assert aggregated_data["clients_on_wireless"] == 8

    mock_ssid_status_calculator.assert_called_once_with(
        ssids=ALL_SSID_DATA, devices=ALL_PROCESSED_DEVICES, relaxed_tag_match=False
    )


@pytest.mark.asyncio
async def test_aggregation_ssid_device_linking_no_mr_devices(aggregator, mock_ssid_status_calculator):
    """Test SSID-device linking when there are no MR devices."""
    non_mr_devices = PROCESSED_DEVICES_MS + PROCESSED_DEVICES_MX
    aggregated_data = await aggregator.aggregate_data(
        processed_devices=non_mr_devices,
        ssid_data=ALL_SSID_DATA,
        network_data=NETWORK_DATA,
        client_data=[],
        network_client_counts={}
    )

    for device in aggregated_data["devices"]:
        assert "ssids" not in device # No MR devices, so no SSIDs should be embedded

    mock_ssid_status_calculator.assert_called_once_with(
        ssids=ALL_SSID_DATA, devices=non_mr_devices, relaxed_tag_match=False
    )

@pytest.mark.asyncio
async def test_aggregation_ssid_device_linking_ssids_not_in_device_network(aggregator, mock_ssid_status_calculator):
    """Test SSID-device linking ensuring only SSIDs of the device's network are linked."""
    # MR1 is in N1. SSID_DATA_N2 are for network N2.
    mr1_device_list = [PROCESSED_DEVICES_MR[0]] # Only MR1

    aggregated_data = await aggregator.aggregate_data(
        processed_devices=mr1_device_list,
        ssid_data=ALL_SSID_DATA, # Contains SSIDs from N1 and N2
        network_data=NETWORK_DATA,
        client_data=[],
        network_client_counts={}
    )

    mr1_aggregated = next(d for d in aggregated_data["devices"] if d["serial"] == "MR1")
    assert "ssids" in mr1_aggregated
    # Should only contain SSIDs from N1
    assert len(mr1_aggregated["ssids"]) == len(SSID_DATA_N1)
    for ssid_in_device in mr1_aggregated["ssids"]:
        assert ssid_in_device["networkId"] == "N1"

    mock_ssid_status_calculator.assert_called_once_with(
        ssids=ALL_SSID_DATA, devices=mr1_device_list, relaxed_tag_match=False
    )

# print("test_data_aggregator.py created") # Removed print
