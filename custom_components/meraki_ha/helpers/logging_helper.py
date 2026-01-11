"""Centralized logging configuration for the Meraki integration.

This module provides feature-specific loggers that can be individually controlled
in Home Assistant's logger configuration OR via the integration's options flow.

Example configuration.yaml:
```yaml
logger:
  default: info
  logs:
    # Main integration
    custom_components.meraki_ha: info

    # Feature-specific logging (add any of these to adjust verbosity):
    custom_components.meraki_ha.mqtt: warning       # Silence MQTT spam
    custom_components.meraki_ha.alerts: debug       # Webhook alerts
    custom_components.meraki_ha.scanning_api: debug # Scanning API/CMX
    custom_components.meraki_ha.api: debug          # Debug API calls
    custom_components.meraki_ha.coordinator: info   # Data coordinator updates
    custom_components.meraki_ha.device_tracker: warning  # Client tracking
    custom_components.meraki_ha.discovery: info     # Device/entity discovery
    custom_components.meraki_ha.camera: debug       # Camera operations
    custom_components.meraki_ha.sensor: info        # Sensor updates
    custom_components.meraki_ha.switch: debug       # Switch/toggle entities
    custom_components.meraki_ha.frontend: debug     # Frontend panel
```

Note: Log levels can also be configured via the integration's options flow
(Settings → Devices & Services → Meraki → Configure → Logging).
"""

from __future__ import annotations

import logging
from typing import Final

# Base domain for all loggers
_BASE_DOMAIN: Final = "custom_components.meraki_ha"


def get_logger(feature: str | None = None) -> logging.Logger:
    """Get a logger for a specific feature.

    Args:
        feature: The feature name (e.g., 'mqtt', 'webhook', 'api').
                 If None, returns the base integration logger.

    Returns
    -------
        A logging.Logger instance for the specified feature.

    Example
    -------
        >>> from custom_components.meraki_ha.helpers.logging_helper import get_logger
        >>> _LOGGER = get_logger("mqtt")
        # Returns logger for custom_components.meraki_ha.mqtt

    """
    if feature:
        return logging.getLogger(f"{_BASE_DOMAIN}.{feature}")
    return logging.getLogger(_BASE_DOMAIN)


# Pre-defined feature loggers for common use cases
# These can be imported directly for convenience


class MerakiLoggers:
    """Collection of pre-configured feature loggers.

    Usage:
        from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

        _LOGGER = MerakiLoggers.MQTT
        _LOGGER.debug("MQTT message received")
    """

    # Core features
    MAIN: Final = logging.getLogger(_BASE_DOMAIN)
    """Main integration logger."""

    API: Final = logging.getLogger(f"{_BASE_DOMAIN}.api")
    """API calls to Meraki cloud."""

    COORDINATOR: Final = logging.getLogger(f"{_BASE_DOMAIN}.coordinator")
    """Data coordinator updates and polling."""

    # Communication features
    MQTT: Final = logging.getLogger(f"{_BASE_DOMAIN}.mqtt")
    """MQTT service for MT sensor real-time updates."""

    ALERTS: Final = logging.getLogger(f"{_BASE_DOMAIN}.alerts")
    """Webhook alerts from Meraki Dashboard."""

    SCANNING_API: Final = logging.getLogger(f"{_BASE_DOMAIN}.scanning_api")
    """Scanning API (CMX) client presence updates."""

    # Legacy alias for backwards compatibility
    WEBHOOK: Final = logging.getLogger(f"{_BASE_DOMAIN}.webhook")
    """Legacy webhook logger - use ALERTS or SCANNING_API instead."""

    # Entity features
    DEVICE_TRACKER: Final = logging.getLogger(f"{_BASE_DOMAIN}.device_tracker")
    """Client device tracking."""

    CAMERA: Final = logging.getLogger(f"{_BASE_DOMAIN}.camera")
    """Camera operations (snapshots, streams)."""

    SENSOR: Final = logging.getLogger(f"{_BASE_DOMAIN}.sensor")
    """Sensor entity updates."""

    SWITCH: Final = logging.getLogger(f"{_BASE_DOMAIN}.switch")
    """Switch/toggle entity operations."""

    # Infrastructure
    DISCOVERY: Final = logging.getLogger(f"{_BASE_DOMAIN}.discovery")
    """Device and entity discovery."""

    FRONTEND: Final = logging.getLogger(f"{_BASE_DOMAIN}.frontend")
    """Frontend panel and web UI."""


# Feature name constants for documentation
FEATURE_NAMES: Final[dict[str, str]] = {
    "mqtt": "MQTT real-time sensor updates",
    "alerts": "Webhook alerts from Meraki Dashboard",
    "scanning_api": "Scanning API (CMX) client presence",
    "api": "Meraki cloud API calls",
    "coordinator": "Data polling and updates",
    "device_tracker": "Client device tracking",
    "camera": "Camera snapshots and streams",
    "sensor": "Sensor entity updates",
    "switch": "Switch/toggle operations",
    "discovery": "Device and entity discovery",
    "frontend": "Frontend panel and web UI",
}

# Mapping from log level string to Python logging level
_LOG_LEVEL_MAP: Final[dict[str, int]] = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# Mapping from config option keys to logger feature names
_CONFIG_TO_LOGGER_MAP: Final[dict[str, logging.Logger]] = {
    "log_level_mqtt": MerakiLoggers.MQTT,
    "log_level_alerts": MerakiLoggers.ALERTS,
    "log_level_scanning_api": MerakiLoggers.SCANNING_API,
    "log_level_api": MerakiLoggers.API,
    "log_level_coordinator": MerakiLoggers.COORDINATOR,
    "log_level_device_tracker": MerakiLoggers.DEVICE_TRACKER,
    "log_level_discovery": MerakiLoggers.DISCOVERY,
    "log_level_camera": MerakiLoggers.CAMERA,
    "log_level_sensor": MerakiLoggers.SENSOR,
    "log_level_switch": MerakiLoggers.SWITCH,
    "log_level_frontend": MerakiLoggers.FRONTEND,
}


def apply_log_levels(options: dict[str, str]) -> None:
    """Apply log levels from integration options to feature loggers.

    This function is called when logging options are saved or when
    the integration starts up.

    Args:
    ----
        options: Dictionary of integration options containing log level settings.

    Example
    -------
        >>> apply_log_levels({"log_level_mqtt": "warning", "log_level_api": "debug"})

    """
    for config_key, logger in _CONFIG_TO_LOGGER_MAP.items():
        level_str = options.get(config_key, "info")
        level = _LOG_LEVEL_MAP.get(level_str, logging.INFO)
        logger.setLevel(level)
        logger.debug("Set log level to %s", level_str.upper())
