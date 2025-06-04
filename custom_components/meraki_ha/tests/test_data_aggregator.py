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
    mock_data_processor, mock_ssid_status_calculator_unused
):  # mock_ssid_status_calculator_unused is to trigger its patching
    # The SsidStatusCalculator instance passed to DataAggregator isn't directly used for its methods
    # if SsidStatusCalculator.calculate_ssid_status is a static method and patched directly.
    # However, we still need to pass an instance.
    # We use mock_ssid_status_calculator_unused to ensure the static method is patched during this test.
    return DataAggregator(
        relaxed_tag_match=False,
        data_processor=mock_data_processor,
        ssid_status_calculator=MagicMock(
            spec=SsidStatusCalculator
        ),  # Pass a mock instance
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

print("test_data_aggregator.py created")
