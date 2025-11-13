"""Tests for the Meraki integration refactoring."""

from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import CONF_SCAN_INTERVAL, DATA_CLIENT, DOMAIN


async def test_successful_setup(hass: HomeAssistant, enable_custom_integrations: None):
    """Test that the integration is set up successfully after refactoring."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test_api_key", "meraki_org_id": "org_id"},
        options={CONF_SCAN_INTERVAL: 300},
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)

    with patch("custom_components.meraki_ha.MerakiAPIClient") as mock_api_client, patch(
        "custom_components.meraki_ha.discovery.service.DeviceDiscoveryService.discover_entities",
        return_value=[],
    ), patch(
        "custom_components.meraki_ha.webhook.async_register_webhook"
    ) as mock_register_webhook, patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
    ) as mock_forward_setups:
        mock_api_client.return_value.get_all_data = AsyncMock(
            return_value={
                "devices": [],
                "networks": [],
                "ssids": [],
                "clients": [],
                "vlans": {},
                "appliance_uplink_statuses": [],
                "rf_profiles": {},
            }
        )

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Verify that the domain data is set up
        assert DOMAIN in hass.data
        assert entry.entry_id in hass.data[DOMAIN]

        # Verify that the coordinators and services are created
        entry_data = hass.data[DOMAIN][entry.entry_id]
        assert "coordinator" in entry_data
        assert "meraki_repository" in entry_data
        assert "control_service" in entry_data
        assert "camera_service" in entry_data
        assert "network_control_service" in entry_data
        assert DATA_CLIENT in entry_data
        assert "discovery_service" in entry_data

        # Verify that discovery was run
        assert "entities" in entry_data

        # Verify that platforms are set up
        mock_forward_setups.assert_called_once()


async def test_reconfiguration(hass: HomeAssistant, enable_custom_integrations: None):
    """Test that the integration is reconfigured successfully."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test_api_key", "meraki_org_id": "org_id"},
        options={CONF_SCAN_INTERVAL: 300},
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)

    with patch("custom_components.meraki_ha.MerakiAPIClient") as mock_api_client, patch(
        "custom_components.meraki_ha.discovery.service.DeviceDiscoveryService.discover_entities",
        return_value=[],
    ), patch("custom_components.meraki_ha.webhook.async_register_webhook"), patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
    ):
        mock_api_client.return_value.get_all_data = AsyncMock(
            return_value={
                "devices": [],
                "networks": [],
                "ssids": [],
                "clients": [],
                "vlans": {},
                "appliance_uplink_statuses": [],
                "rf_profiles": {},
            }
        )

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        original_coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
        original_api_client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]

    # Reconfigure by updating options
    from datetime import timedelta

    new_options = entry.options.copy()
    new_options[CONF_SCAN_INTERVAL] = 100

    with patch(
        "custom_components.meraki_ha.MerakiAPIClient", new=mock_api_client
    ), patch(
        "custom_components.meraki_ha.discovery.service.DeviceDiscoveryService.discover_entities",
        return_value=[],
    ), patch("custom_components.meraki_ha.webhook.async_register_webhook"), patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
    ):
        hass.config_entries.async_update_entry(entry, options=new_options)
        await hass.async_block_till_done()

    # Assertions
    assert hass.data[DOMAIN][entry.entry_id]["coordinator"] is original_coordinator
    assert hass.data[DOMAIN][entry.entry_id][DATA_CLIENT] is original_api_client
    assert hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ].update_interval == timedelta(seconds=100)
