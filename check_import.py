import os
import sys
import logging

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
_LOGGER = logging.getLogger("import_check")

# Add the parent directory of custom_components to sys.path
sys.path.append(os.getcwd())

try:
    from custom_components.meraki_ha.core.api.client import (
        MerakiAPIClient,  # noqa: F401
    )

    _LOGGER.info("Successfully imported MerakiAPIClient")
except ImportError as e:
    _LOGGER.error("ImportError: %s", e)
    sys.exit(1) # Exit with error code for CI/CD pipelines
except Exception as e:
    _LOGGER.exception("Unexpected exception during import: %s", e)
    sys.exit(1)