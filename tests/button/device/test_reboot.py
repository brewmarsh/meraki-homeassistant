"""Test the Meraki reboot button."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_coordinator():
    """Mock the Meraki Data Coordinator."""
    coordinator = MagicMock()
    coordinator.data = {}
    return coordinator


@pytest.fixture
def mock_device():
    """Mock a MerakiDevice."""
    return MerakiDevice(
        serial="Q2XX-XXXX-XXXX",
        name="Test Device",
        model="MX67",
        mac="00:11:22:33:44:55",
        product_type="appliance",
        status="online"
    )


@pytest.fixture
def mock_control_service():
    """Mock the DeviceControlService."""
    service = MagicMock()
    service.async_reboot = AsyncMock()
    return service


@pytest.fixture
def mock_config_entry():
    """Mock a ConfigEntry."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.options = {}
    return entry


async def test_reboot_button_initialization(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_control_service: MagicMock,
    mock_device: MerakiDevice,
    mock_config_entry: ConfigEntry,
):
    """Test the button initialization."""
    button = MerakiRebootButton(
        mock_coordinator, mock_control_service, mock_device, mock_config_entry
    )

    assert button.name == "Reboot"
    assert button.unique_id == "Q2XX-XXXX-XXXX_merakirebootbutton"


async def test_reboot_button_availability(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_control_service: MagicMock,
    mock_device: MerakiDevice,
    mock_config_entry: ConfigEntry,
):
    """Test the button availability."""
    # Setup coordinator data for MerakiEntity availability
    mock_coordinator.data = {
        "devices_by_serial": {
            "Q2XX-XXXX-XXXX": mock_device
        }
    }

    button = MerakiRebootButton(
        mock_coordinator, mock_control_service, mock_device, mock_config_entry
    )
    button.hass = hass
    button.entity_id = "button.test_reboot"

    # MX67 has "reboot" capability
    assert button.available is True

    # MT10 does NOT have "reboot" capability
    mock_device.model = "MT10"
    # Need to trigger update because button stores its own _device
    button._handle_coordinator_update()
    assert button.available is False

    # Device offline - should STILL be available for reboot buttons if model is correct
    mock_device.model = "MX67"
    button._handle_coordinator_update()
    mock_device.status = "offline"
    assert button.available is True


async def test_reboot_button_press(
    hass: HomeAssistant,
    mock_coordinator: MagicMock,
    mock_control_service: MagicMock,
    mock_device: MerakiDevice,
    mock_config_entry: ConfigEntry,
):
    """Test the button press action."""
    button = MerakiRebootButton(
        mock_coordinator, mock_control_service, mock_device, mock_config_entry
    )

    await button.async_press()

    mock_control_service.async_reboot.assert_called_once_with("Q2XX-XXXX-XXXX")
