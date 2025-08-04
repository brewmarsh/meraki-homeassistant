# Design Document

This document outlines the design of the Meraki Home Assistant integration.

## Overview

The Meraki Home Assistant integration allows users to monitor and control their Meraki networks and devices within Home Assistant. The integration is built around a central data update coordinator that fetches data from the Meraki API and distributes it to the various platforms (e.g., sensor, switch, device_tracker).

## Architecture

The integration is divided into the following components:

*   **`__init__.py`**: The main entry point for the integration. It sets up the coordinators and platforms.
*   **`core`**: A directory containing the core components of the integration, including the API client, coordinators, and entities.
*   **`api`**: A wrapper around the Meraki Dashboard API that provides a simplified interface for making API calls. This is implemented in the `core/api/client.py` file.
*   **`coordinators`**: The data update coordinators that fetch data from the Meraki API and manage the state of the integration. These are implemented in the `core/coordinators` directory.
*   **`entities`**: The base classes for the entities in the integration. These are implemented in the `core/entities` directory.
*   **`platforms`**: The platform-specific implementations of the entities, such as sensors, switches, and device trackers.
*   **`const.py`**: A file that contains all of the constants used in the integration.
*   **`AGENTS.md`**: A file that contains guidelines for agents working on the codebase.

## Error Handling

The integration uses a centralized error handling strategy to ensure that all errors are handled consistently and that user-friendly error messages are displayed. The `@handle_meraki_errors` decorator is used to wrap all API calls and to handle any errors that may occur. The decorator logs the errors and raises a more specific exception from the `core.errors` module. This allows the calling code to handle different types of errors in a more granular way.

## Data Flow

The integration uses a hybrid data retrieval strategy that combines polling with webhooks.

*   **Polling:** The `MerakiDataUpdateCoordinator` fetches data from the Meraki API at a regular interval. This is used to get the initial state of the integration and to periodically refresh the data.
*   **Webhooks:** The integration also uses webhooks to receive real-time updates from the Meraki API. This is used to get real-time updates for things like device status and client connectivity.

The data flow for the integration is as follows:

1.  The `MerakiDeviceCoordinator` and `MerakiNetworkCoordinator` fetch data from the Meraki API at a regular interval.
2.  Each coordinator stores its data in its own `data` attribute.
3.  The platforms (e.g., sensor, switch, device_tracker) access the data from the appropriate coordinator and update their state accordingly.
4.  The integration also receives real-time updates from the Meraki API via webhooks.
5.  The `async_handle_webhook` function processes the data from the webhook and updates the state of the integration accordingly.

## Coordinators

The integration uses two coordinators, which are located in the `core/coordinators` directory:

*   **`MerakiDeviceCoordinator`**: This coordinator is responsible for fetching data for all physical Meraki devices in the organization. It fetches base device data, and then enhances it with device-specific data like port statuses for switches, uplink information for appliances, and sensor readings for MT sensors.
*   **`MerakiNetworkCoordinator`**: This coordinator fetches data for all networks, clients, and SSIDs in the organization. It also filters out disabled SSIDs.

## Platforms

The integration provides the following platforms:

*   **`sensor`**: The sensor platform provides sensors for monitoring the following:
    *   The status of Meraki devices (e.g., online, offline).
    *   The number of clients connected to each device.
    *   The status of the WAN connection for MX devices.
    *   Data usage for MX appliances.
    *   PoE usage for MS switches.
    *   Port counts (in use/available) for MS switches.
    *   The radio settings for MR devices.
    *   The status of the SSIDs.
    *   Environmental readings (temperature, humidity, water detection) for MT sensors.
*   **`switch`**: The switch platform provides switches for controlling the following:
    *   The state of the SSIDs (e.g., enabled, disabled).
    *   The broadcast state of the SSIDs.
    *   The state of the camera sense feature for MV cameras.
    *   The state of the audio detection feature for MV cameras.
    *   The state of the RTSP server for MV cameras.
*   **`device_tracker`**: The device tracker platform provides device trackers for monitoring the presence of clients on the network.
*   **`text`**: The text platform provides text entities for displaying the following:
    *   The name of the SSIDs.
    *   The status of the SSIDs.

## Code Duplication and Refactoring Opportunities

### Device Sensor Base Class

The device sensor platforms in `custom_components/meraki_ha/sensor/device` have a lot of duplicated code. A base class could be created to handle the following:

*   **`__init__` method:** The base class could handle the common initialization logic, such as setting the unique ID, name, and icon.
*   **`device_info` property:** The base class could provide a default implementation of the `device_info` property.
*   **`_handle_coordinator_update` method:** The base class could provide a default implementation of the `_handle_coordinator_update` method.
*   **`available` property:** The base class could provide a default implementation of the `available` property.
*   **`_get_current_device_data` method:** The base class could provide a helper method to get the current device data from the coordinator.

By creating a base class, we can significantly reduce the amount of duplicated code and make the sensor platforms easier to maintain.
