# meraki_api.py
import logging

from meraki import DashboardAPI
from meraki.exceptions import APIError

# from ValueError import ValueError
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)  # Create a logger instance


async def validate_meraki_credentials(api_key, org_id):
    """Validate Meraki API credentials."""
    _LOGGER.debug("Validating Meraki credentials")  # Add logging
    try:
        dashboard = DashboardAPI(
            api_key=api_key,
            base_url="https://api.meraki.com/api/v1/",
            print_console=False,
            output_log=False,
            suppress_logging=True,
        )

        organizations = dashboard.organizations.getOrganizations()
        _LOGGER.debug(f"Organizations: {organizations}")  # Log organizations

        if not any(org["id"] == org_id for org in organizations):
            _LOGGER.error("Invalid Organization ID")  # Log error
            raise ValueError("Invalid Organization ID")
        _LOGGER.debug("Credentials validated successfully")
        return True
    except APIError as e:
        if e.status == 401:
            raise ConfigEntryAuthFailed
        raise Exception(f"Meraki API Error: {e.message}")
    except Exception as e:
        raise Exception(f"Error connecting to Meraki API: {e}")


async def get_meraki_devices(api_key, org_id):
    """Retrieves all devices from a Meraki organization."""
    try:
        dashboard = DashboardAPI(
            api_key=api_key,
            base_url="https://api.meraki.com/api/v1/",
            print_console=False,
            output_log=False,
            suppress_logging=True,
        )
        devices = dashboard.organizations.getOrganizationDevices(organizationId=org_id)
        return devices
    except Exception as e:
        raise Exception(f"Error retrieving Meraki devices: {e}")
