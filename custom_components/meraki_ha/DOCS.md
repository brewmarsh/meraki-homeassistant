# Meraki HA Integration - Technical Overview

## Introduction

This document provides a technical overview of the Meraki Home Assistant integration (`meraki_ha`). It is intended for developers, contributors, or anyone interested in understanding the internal structure and core components of this integration.

For user-facing documentation, including setup instructions, features, and troubleshooting, please refer to the main `README.md` file at the root of this repository. More comprehensive user guides will be available on our MkDocs site (link to be added once live).

## Core Components

The Meraki HA integration is structured as a standard Home Assistant custom component. Key directories and files within `custom_components/meraki_ha/` include:

*   **`__init__.py`**:
    *   The main entry point for the integration.
    *   Handles the overall setup of the integration when Home Assistant starts or when a config entry is added.
    *   Manages the forwarding of the setup process to the relevant entity platforms (sensor, switch, device_tracker).

*   **`coordinator.py`** (and the **`coordinators/`** directory):
    *   Defines the `MerakiDataUpdateCoordinator` which is central to the integration.
    *   Responsible for fetching data from the Meraki API at regular intervals.
    *   Processes and aggregates data from various API endpoints (devices, networks, SSIDs, clients, etc.).
    *   Manages subordinate coordinators (found in the `coordinators/` directory) that may handle specific aspects of data fetching, processing, or actions (e.g., tag updates, data aggregation).
    *   Notifies registered entities when new data is available.

*   **`meraki_api/`** directory:
    *   Contains modules dedicated to direct interaction with the Cisco Meraki Dashboard API.
    *   Abstracts the API calls into Python functions (e.g., fetching devices, networks, SSIDs, updating tags).
    *   Includes an API client (`_api_client.py`) for making HTTP requests and handling responses/errors.
    *   Defines custom exceptions for API-related issues.

*   **`sensor/`**, **`switch/`**, **`device_tracker/`** directories:
    *   Implement the Home Assistant entity platforms.
    *   Each directory contains the code for specific entity types:
        *   `sensor/`: Entities that represent state or measurements from Meraki devices/networks (e.g., device status, client counts, uplink status, SSID availability).
        *   `switch/`: Entities that allow control over Meraki features (e.g., enabling/disabling SSIDs via device tags).
        *   `device_tracker/`: Entities that represent Meraki network devices themselves for presence detection (based on client connectivity to the device).

*   **`config_flow.py`**:
    *   Manages the user configuration process when the integration is added to Home Assistant via the UI.
    *   Handles user input for essential details like the Meraki API Key and Organization ID.
    *   Includes logic for validating credentials.
    *   Manages the options flow, allowing users to modify settings (e.g., scan interval, device name format) after initial setup.

*   **`const.py`**:
    *   Defines core constants used throughout the integration.
    *   Includes the integration domain, configuration keys, default values, platform names, and other static strings to ensure consistency and avoid magic strings in the code.

*   **`entity.py`**:
    *   Provides a base `MerakiEntity` class that other Meraki-specific entities inherit from.
    *   Includes common functionality such as linking to the `MerakiDataUpdateCoordinator` and setting up device information for the Home Assistant device registry.

*   **`helpers/`** directory:
    *   Contains utility modules and helper classes that support various functions within the integration.
    *   For example, `ssid_status_calculator.py` which determines the operational state of SSIDs based on device tags.

*   **`authentication.py`**:
    *   Provides functionality for validating Meraki API credentials (API Key and Organization ID) against the Meraki cloud.

*   **`device_setup.py`** and **`network_setup.py`**:
    *   These files contain older or potentially supplementary logic for setting up device and network representations in Home Assistant. Their functionality might overlap with or be superseded by the more recent coordinator-based setup in `__init__.py` and the respective platform setup files. Review and refactoring may be needed to consolidate device/network registration.

## Key Concepts

*   **Data Update Coordinator (`MerakiDataUpdateCoordinator`)**: This is the heart of the data management. It polls the Meraki API periodically and makes the latest data available to all entities. This reduces redundant API calls from individual entities.
*   **Device Identification**: Meraki devices are primarily identified by their unique **serial number**. This is used for API calls and for creating unique identifiers in Home Assistant's device registry.
*   **SSID to Device Matching (for Switches)**: The `MerakiSSIDSwitch` entities control SSIDs on specific devices. The decision to create a switch for an SSID on a device is handled by the `match_device_to_ssid` function. This logic typically involves:
    *   Checking for specific tags on the Meraki device.
    *   Comparing these device tags against tags defined in the SSID's configuration (if any).
    *   A "relaxed matching" option allows an SSID to be matched if *any* of its defined tags are present on the device, versus strict matching which requires *all* SSID tags to be on the device.
    *   SSID state (enabled/disabled) is controlled by adding or removing a specific tag (e.g., `ssid_MySSID_enabled`) on the device.
*   **Entity Base Class (`MerakiEntity`)**: Provides common boilerplate for Meraki entities, such as linking to the coordinator and providing standard device information for the HA device registry.

## Development Prerequisites

To develop or test this integration locally, you will need:

1.  **Meraki API Key**: Obtain this from your Meraki Dashboard (Organization > Settings > API access).
2.  **Meraki Organization ID**: This can be found in the URL when logged into your Meraki Dashboard or via API calls.
3.  **Familiarity with Home Assistant Custom Components**: Understanding the basic structure, lifecycle, and core concepts of Home Assistant custom component development is essential. Refer to the [Home Assistant Developer Documentation](https://developers.home-assistant.com/).
4.  A development environment for Home Assistant (e.g., a local HA Core installation, a dev container, or a VM).

## Further Documentation

*   **Main User Guide**: For installation, setup, and usage instructions, please see the [README.md](../../README.md) at the root of this repository.
*   **Detailed Technical Documentation & User Guides**: Detailed user guides, in-depth configuration instructions, entity explanations, and troubleshooting tips will be available at **[Link to MkDocs site - to be added once live]**.

This document serves as a high-level technical guide. For specific implementation details, please refer to the source code and the inline docstrings within each module.
