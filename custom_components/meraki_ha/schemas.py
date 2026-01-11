"""Schema definitions for the Meraki Home Assistant integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import selector

from .const import (
    CONF_CAMERA_LINK_INTEGRATION,
    CONF_CAMERA_SNAPSHOT_INTERVAL,
    CONF_CLIENT_SCAN_INTERVAL,
    CONF_DASHBOARD_DEVICE_TYPE_FILTER,
    CONF_DASHBOARD_STATUS_FILTER,
    CONF_DASHBOARD_VIEW_MODE,
    CONF_DEVICE_SCAN_INTERVAL,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_MQTT,
    CONF_ENABLE_SCANNING_API,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_NETWORK_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL,
    CONF_SCANNING_API_SECRET,
    CONF_SCANNING_API_VALIDATOR,
    CONF_SSID_SCAN_INTERVAL,
    CONF_TEMPERATURE_UNIT,
    DASHBOARD_VIEW_MODE_NETWORK,
    DASHBOARD_VIEW_MODE_TYPE,
    DEFAULT_CAMERA_LINK_INTEGRATION,
    DEFAULT_CAMERA_SNAPSHOT_INTERVAL,
    DEFAULT_CLIENT_SCAN_INTERVAL,
    DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER,
    DEFAULT_DASHBOARD_STATUS_FILTER,
    DEFAULT_DASHBOARD_VIEW_MODE,
    DEFAULT_DEVICE_SCAN_INTERVAL,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_ENABLE_SCANNING_API,
    DEFAULT_ENABLE_VLAN_MANAGEMENT,
    DEFAULT_ENABLED_NETWORKS,
    DEFAULT_MQTT_PORT,
    DEFAULT_NETWORK_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCANNING_API_SECRET,
    DEFAULT_SCANNING_API_VALIDATOR,
    DEFAULT_SSID_SCAN_INTERVAL,
    DEFAULT_TEMPERATURE_UNIT,
    MQTT_DEST_DEVICE_TYPES,
    MQTT_DEST_HOST,
    MQTT_DEST_NAME,
    MQTT_DEST_PASSWORD,
    MQTT_DEST_PORT,
    MQTT_DEST_TOPIC_FILTER,
    MQTT_DEST_USE_TLS,
    MQTT_DEST_USERNAME,
    TEMPERATURE_UNIT_CELSIUS,
    TEMPERATURE_UNIT_FAHRENHEIT,
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MERAKI_API_KEY): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(CONF_MERAKI_ORG_ID): selector.TextSelector(),
    }
)

# Section: Network Selection
SCHEMA_NETWORK_SELECTION = vol.Schema(
    {
        vol.Optional(
            CONF_ENABLED_NETWORKS, default=DEFAULT_ENABLED_NETWORKS
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[],
                multiple=True,
                custom_value=False,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_ENABLE_DEVICE_TRACKER, default=True
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ENABLE_VLAN_MANAGEMENT, default=DEFAULT_ENABLE_VLAN_MANAGEMENT
        ): selector.BooleanSelector(),
    }
)

# Section: Polling & Refresh
SCHEMA_POLLING = vol.Schema(
    {
        vol.Required(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=30,
                max=300,
                step=5,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.SLIDER,
            )
        ),
        vol.Required(
            CONF_NETWORK_SCAN_INTERVAL, default=DEFAULT_NETWORK_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=300,
                max=3600,
                step=60,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.SLIDER,
            )
        ),
        vol.Required(
            CONF_DEVICE_SCAN_INTERVAL, default=DEFAULT_DEVICE_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=300,
                max=3600,
                step=60,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.SLIDER,
            )
        ),
        vol.Required(
            CONF_CLIENT_SCAN_INTERVAL, default=DEFAULT_CLIENT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=30,
                max=300,
                step=5,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.SLIDER,
            )
        ),
        vol.Required(
            CONF_SSID_SCAN_INTERVAL, default=DEFAULT_SSID_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=300,
                max=3600,
                step=60,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.SLIDER,
            )
        ),
    }
)


# Section: Display Preferences
SCHEMA_DISPLAY_PREFERENCES = vol.Schema(
    {
        vol.Required(
            CONF_DASHBOARD_VIEW_MODE, default=DEFAULT_DASHBOARD_VIEW_MODE
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(
                        value=DASHBOARD_VIEW_MODE_NETWORK, label="By Network"
                    ),
                    selector.SelectOptionDict(
                        value=DASHBOARD_VIEW_MODE_TYPE, label="By Device Type"
                    ),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_DASHBOARD_DEVICE_TYPE_FILTER,
            default=[DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER],
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(value="all", label="All Types"),
                    selector.SelectOptionDict(value="switch", label="Switches"),
                    selector.SelectOptionDict(value="camera", label="Cameras"),
                    selector.SelectOptionDict(value="wireless", label="Wireless APs"),
                    selector.SelectOptionDict(value="sensor", label="Sensors"),
                    selector.SelectOptionDict(value="appliance", label="Appliances"),
                ],
                multiple=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_DASHBOARD_STATUS_FILTER, default=DEFAULT_DASHBOARD_STATUS_FILTER
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(value="all", label="All Statuses"),
                    selector.SelectOptionDict(value="online", label="Online"),
                    selector.SelectOptionDict(value="offline", label="Offline"),
                    selector.SelectOptionDict(value="alerting", label="Alerting"),
                    selector.SelectOptionDict(value="dormant", label="Dormant"),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_TEMPERATURE_UNIT, default=DEFAULT_TEMPERATURE_UNIT
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(
                        value=TEMPERATURE_UNIT_CELSIUS, label="Celsius (°C)"
                    ),
                    selector.SelectOptionDict(
                        value=TEMPERATURE_UNIT_FAHRENHEIT, label="Fahrenheit (°F)"
                    ),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)

# Section: Scanning API Settings
SCHEMA_SCANNING_API = vol.Schema(
    {
        vol.Required(
            CONF_ENABLE_SCANNING_API, default=DEFAULT_ENABLE_SCANNING_API
        ): selector.BooleanSelector(),
        vol.Optional(
            CONF_SCANNING_API_VALIDATOR, default=DEFAULT_SCANNING_API_VALIDATOR
        ): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Optional(
            CONF_SCANNING_API_SECRET, default=DEFAULT_SCANNING_API_SECRET
        ): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
    }
)

SCHEMA_CAMERA = vol.Schema(
    {
        vol.Required(
            CONF_CAMERA_SNAPSHOT_INTERVAL, default=DEFAULT_CAMERA_SNAPSHOT_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                max=3600,
                step=10,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        vol.Optional(
            CONF_CAMERA_LINK_INTEGRATION, default=DEFAULT_CAMERA_LINK_INTEGRATION
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(value="", label="All Cameras"),
                    selector.SelectOptionDict(value="blue_iris", label="Blue Iris"),
                    selector.SelectOptionDict(value="generic", label="Generic Camera"),
                    selector.SelectOptionDict(value="onvif", label="ONVIF"),
                    selector.SelectOptionDict(value="frigate", label="Frigate"),
                    selector.SelectOptionDict(value="unifi", label="UniFi Protect"),
                    selector.SelectOptionDict(value="ring", label="Ring"),
                    selector.SelectOptionDict(value="nest", label="Nest"),
                    selector.SelectOptionDict(value="amcrest", label="Amcrest"),
                    selector.SelectOptionDict(value="reolink", label="Reolink"),
                    selector.SelectOptionDict(value="hikvision", label="Hikvision"),
                    selector.SelectOptionDict(value="dahua", label="Dahua"),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
                custom_value=True,
            )
        ),
    }
)
MQTT_DESTINATION_SCHEMA = vol.Schema(
    {
        vol.Required("server_ip"): selector.TextSelector(),
        vol.Required("port"): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1, max=65535, mode=selector.NumberSelectorMode.BOX
            )
        ),
        vol.Required("topic"): selector.TextSelector(),
    }
)

# Section: MQTT Settings
SCHEMA_MQTT = vol.Schema(
    {
        vol.Required(
            CONF_ENABLE_MQTT, default=DEFAULT_ENABLE_MQTT
        ): selector.BooleanSelector(),
    }
)

# MQTT Relay Destination Schema (used for add/edit destination sub-flow)
MQTT_RELAY_DESTINATION_SCHEMA = vol.Schema(
    {
        vol.Required(MQTT_DEST_NAME): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Required(MQTT_DEST_HOST): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Required(
            MQTT_DEST_PORT, default=DEFAULT_MQTT_PORT
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=65535,
                step=1,
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        vol.Optional(MQTT_DEST_USERNAME): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Optional(MQTT_DEST_PASSWORD): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
        vol.Required(MQTT_DEST_USE_TLS, default=False): selector.BooleanSelector(),
        vol.Required(
            MQTT_DEST_TOPIC_FILTER, default="meraki/v1/mt/#"
        ): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Optional(MQTT_DEST_DEVICE_TYPES): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(
                        value="MT10", label="MT10 (Temp/Humidity)"
                    ),
                    selector.SelectOptionDict(value="MT11", label="MT11 (Temp Probe)"),
                    selector.SelectOptionDict(value="MT12", label="MT12 (Water Leak)"),
                    selector.SelectOptionDict(value="MT14", label="MT14 (Air Quality)"),
                    selector.SelectOptionDict(value="MT15", label="MT15 (Air Quality)"),
                    selector.SelectOptionDict(value="MT20", label="MT20 (Door Sensor)"),
                    selector.SelectOptionDict(value="MT30", label="MT30 (Button)"),
                    selector.SelectOptionDict(
                        value="MT40", label="MT40 (Power Monitor)"
                    ),
                    selector.SelectOptionDict(value="MV", label="MV (Cameras)"),
                ],
                multiple=True,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)
