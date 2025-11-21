# Meraki Home Assistant Integration Architecture

## 1. Overview

This document provides a comprehensive overview of the architecture and design of the `meraki-ha` custom component. The integration is designed for performance, scalability, and resiliency, with a focus on efficient data fetching, centralized state management, and modular design.

## 2. Core Architectural Pillars

-   **Centralized Data Fetching:** A single data coordinator (`MerakiDataCoordinator`) is responsible for all API communication, eliminating redundant API calls and ensuring data consistency.
-   **Optimized API Usage:** The API client (`MerakiAPIClient`) leverages concurrent API calls using `asyncio.gather` to reduce latency and improve responsiveness.
-   **Efficient State Management:** The `MerakiDataCoordinator` creates lookup tables for devices, networks, and SSIDs after each data fetch. This provides entities with fast, O(1) access to their data, avoiding slow, iterative lookups.
-   **Modular Design:** The codebase is broken down into smaller, more focused modules. The API client uses a facade pattern, delegating calls to endpoint-specific handlers. Utility functions and sensor setup logic have also been modularized.
-   **Hybrid Data Retrieval:** The integration uses a hybrid data retrieval strategy that combines polling with webhooks to provide a balance between periodic data refreshes and real-time updates.

## 3. Core Components

### 3.1. `MerakiDataCoordinator`

The heart of the integration is the `MerakiDataCoordinator`, located in `custom_components/meraki_ha/meraki_data_coordinator.py`.

-   **Responsibilities:**
    -   Manages a single, periodic refresh of all data from the Meraki API via the `MerakiAPIClient`.
    -   Holds the complete state of the integration in its `data` attribute.
    -   Creates and maintains lookup tables for efficient data retrieval by entities.
-   **Entity Interaction:** Entities in Home Assistant are subclasses of `CoordinatorEntity` and are linked to the `MerakiDataCoordinator`. They access the coordinator's data to update their state.

### 3.2. `MerakiAPIClient`

The `MerakiAPIClient`, located in `custom_components/meraki_ha/core/api/client.py`, is responsible for all communication with the Meraki Dashboard API.

-   **Design:** It acts as a facade, providing a single entry point for fetching all data (`get_all_data`). It delegates the actual API calls to smaller, endpoint-specific handler classes.
-   **Concurrency:** The client uses `asyncio.gather` and a semaphore to fetch data from multiple API endpoints concurrently, significantly reducing the total time spent waiting for I/O.

### 3.3. Entity and Sensor Setup

-   **`setup_helpers.py`**: The logic for creating all sensor entities is centralized in `custom_components/meraki_ha/sensor/setup_helpers.py`.
-   **`sensor_registry.py`**: The integration uses a sensor registry (`custom_components/meraki_ha/sensor_registry.py`) to explicitly define which sensor classes should be created for each Meraki device type.

## 4. Error Handling and Resiliency

-   **Stale Data on Failure:** If the `MerakiDataCoordinator` fails to fetch an update, it will continue to provide the existing "stale" data for a configurable period (default 30 minutes).
-   **Partial Data Merging:** If one of the concurrent API sub-requests fails, the integration will use the data from the last successful run for that specific slice of data, preventing a single failure from making an entire category of sensors unavailable.
-   **Persistent Caching:** The integration uses a persistent disk cache (`diskcache`) to improve startup times.

## 5. Webhook Implementation

The integration has a functional webhook implementation for real-time updates. It can register a webhook with the Meraki API and handle incoming alerts for "APs went down" and "Client connectivity changed".

## 6. Code Duplication and Refactoring Opportunities

### 6.1. Device Sensor Base Class

The device sensor platforms in `custom_components/meraki_ha/sensor/device` have a lot of duplicated code. A base class could be created to handle common initialization logic, `device_info` property, `_handle_coordinator_update` method, `available` property, and a helper method to get the current device data from the coordinator.
