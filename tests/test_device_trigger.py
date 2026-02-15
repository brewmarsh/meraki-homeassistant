"""The tests for Meraki device triggers."""
from __future__ import annotations

import pytest
from homeassistant.components import automation
from homeassistant.components.device_automation import DeviceAutomationType
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_get_device_automations,
    async_mock_service,
)

from custom_components.meraki_ha.const import DOMAIN, EVENT_MERAKI_WEBHOOK_ALERT


@pytest.fixture
def device_reg(hass: HomeAssistant) -> dr.DeviceRegistry:
    """Return an empty, loaded, registry."""
    return dr.async_get(hass)


@pytest.fixture
def service_calls(hass: HomeAssistant) -> list[ServiceCall]:
    """Track calls to a mock service."""
    return async_mock_service(hass, "test", "automation")


@pytest.mark.asyncio
async def test_get_triggers(
    hass: HomeAssistant,
    device_reg: dr.DeviceRegistry,
    enable_custom_integrations: None,
) -> None:
    """Test we get the expected triggers from a Meraki device."""
    config_entry = MockConfigEntry(domain=DOMAIN, data={})
    config_entry.add_to_hass(hass)
    device_entry = device_reg.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, "Q234-ABCD-5678")},
        name="Test Device",
        manufacturer="Meraki",
        model="MR33",
    )

    expected_trigger = {
        CONF_PLATFORM: "device",
        CONF_DOMAIN: DOMAIN,
        CONF_TYPE: "meraki_alert",
        CONF_DEVICE_ID: device_entry.id,
        "metadata": {},
    }

    triggers = await async_get_device_automations(
        hass, DeviceAutomationType.TRIGGER, device_entry.id
    )
    assert expected_trigger in triggers


@pytest.mark.asyncio
async def test_fire_trigger_device_alert(
    hass: HomeAssistant,
    device_reg: dr.DeviceRegistry,
    enable_custom_integrations: None,
    service_calls: list[ServiceCall],
) -> None:
    """Test for device alert triggers firing."""
    config_entry = MockConfigEntry(domain=DOMAIN, data={})
    config_entry.add_to_hass(hass)
    device_entry = device_reg.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, "Q234-ABCD-5678")},
    )

    assert await async_setup_component(hass, "trace", {})
    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        CONF_PLATFORM: "device",
                        CONF_DOMAIN: DOMAIN,
                        CONF_DEVICE_ID: device_entry.id,
                        CONF_TYPE: "meraki_alert",
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {"some": "{{ trigger.payload.alertType }}"},
                    },
                }
            ]
        },
    )

    # Fire event for this device
    hass.bus.async_fire(
        EVENT_MERAKI_WEBHOOK_ALERT,
        {
            "alertType": "APs went down",
            "deviceSerial": "Q234-ABCD-5678",
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 1
    assert service_calls[0].data["some"] == "APs went down"

    # Fire event for another device
    hass.bus.async_fire(
        EVENT_MERAKI_WEBHOOK_ALERT,
        {
            "alertType": "APs went down",
            "deviceSerial": "OTHER-SERIAL",
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 1  # Should not increase


@pytest.mark.asyncio
async def test_fire_trigger_network_alert(
    hass: HomeAssistant,
    device_reg: dr.DeviceRegistry,
    enable_custom_integrations: None,
    service_calls: list[ServiceCall],
) -> None:
    """Test for network alert triggers firing."""
    config_entry = MockConfigEntry(domain=DOMAIN, data={})
    config_entry.add_to_hass(hass)
    # Create a network device
    network_id = "N_12345"
    device_entry = device_reg.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, f"network_{network_id}")},
        name="Test Network",
        model="Meraki Network",
    )

    assert await async_setup_component(hass, "trace", {})
    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        CONF_PLATFORM: "device",
                        CONF_DOMAIN: DOMAIN,
                        CONF_DEVICE_ID: device_entry.id,
                        CONF_TYPE: "meraki_alert",
                    },
                    "action": {
                        "service": "test.automation",
                        "data": {"msg": "network alert"},
                    },
                }
            ]
        },
    )

    # Fire event for this network
    hass.bus.async_fire(
        EVENT_MERAKI_WEBHOOK_ALERT,
        {
            "alertType": "Network alert",
            "networkId": network_id,
            # No deviceSerial for network-wide alerts typically, or irrelevant
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 1
    assert service_calls[0].data["msg"] == "network alert"
