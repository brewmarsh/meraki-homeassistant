# Design Document

This document outlines the design of the Meraki Home Assistant integration.

## Overview

The Meraki Home Assistant integration allows users to monitor and control their Meraki networks and devices within Home Assistant. The integration is built around a central data update coordinator that fetches data from the Meraki API and distributes it to the various platforms (e.g., sensor, switch, device_tracker).

## Architecture

The integration is divided into the following components:

*   **`__init__.py`**: The main entry point for the integration. It sets up the coordinators and platforms.
*   **`api`**: A wrapper around the Meraki Dashboard API that provides a simplified interface for making API calls.
*   **`coordinators`**: The data update coordinators that fetch data from the Meraki API and manage the state of the integration.
*   **`sensor`**: The sensor platform, which provides sensors for monitoring the status of Meraki devices and networks.
*   **`switch`**: The switch platform, which provides switches for controlling Meraki devices and SSIDs.
*   **`device_tracker`**: The device tracker platform, which provides device trackers for monitoring the presence of clients on the network.
*   **`text`**: The text platform, which provides text entities for displaying information about Meraki devices and SSIDs.
*   **`const.py`**: A file that contains all of the constants used in the integration.
*   **`AGENTS.md`**: A file that contains guidelines for agents working on the codebase.

## Data Flow

The data flow for the integration is as follows:

1.  The `MerakiDataUpdateCoordinator` fetches data from the Meraki API at a regular interval.
2.  The coordinator stores the data in its `data` attribute.
3.  The platforms (e.g., sensor, switch, device_tracker) access the data from the coordinator and update their state accordingly.

## Coordinators

The integration uses two coordinators:

*   **`MerakiDataUpdateCoordinator`**: The main coordinator that fetches data for all of the devices and networks in the organization.
*   **`SSIDDeviceCoordinator`**: A coordinator that fetches data for the SSIDs in the organization.

## Platforms

The integration provides the following platforms:

*   **`sensor`**: The sensor platform provides sensors for monitoring the following:
    *   The status of Meraki devices (e.g., online, offline).
    *   The number of clients connected to each device.
    *   The status of the WAN connection for MX devices.
    *   The radio settings for MR devices.
    *   The status of the SSIDs.
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
