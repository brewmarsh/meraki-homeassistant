import sys

sys.path.append(".")
from unittest.mock import MagicMock

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.entity import MerakiEntity


def check():
    """Run test script."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices_by_serial": {
            "123": {"serial": "123", "status": "offline", "model": "MS120"}
        }
    }

    # Test Base Meraki Entity
    entity = MerakiEntity(coordinator)
    entity._serial = "123"
    entity.name = "Test Entity"

    print(f"Base Entity Available (offline device): {entity.available}")

    # Test Reboot Button
    device_data = {"serial": "123", "status": "offline", "model": "MS120"}
    btn = MerakiRebootButton(coordinator, MagicMock(), device_data, MagicMock())
    btn._serial = "123"
    btn.name = "Test Reboot Button"
    btn.coordinator = coordinator
    print(f"Reboot Button Available (offline device): {btn.available}")


check()
