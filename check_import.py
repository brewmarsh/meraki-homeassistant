import os
import sys

# Add the parent directory of custom_components to sys.path
sys.path.append(os.getcwd())

try:
    from custom_components.meraki_ha.core.api.client import MerakiAPIClient
    print("Successfully imported MerakiAPIClient")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")
