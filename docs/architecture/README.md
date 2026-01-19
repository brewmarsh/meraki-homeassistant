# Architecture Overview for `meraki-ha`

## 1. Executive Summary

This document provides an overview of the architecture for the `meraki-ha` custom component. The integration is designed for performance and scalability, with a focus on efficient data fetching, centralized state management, and modular design.

The key architectural pillars are:

- **Centralized Data Fetching:** A single data coordinator (`MerakiDataCoordinator`) is responsible for all API communication, eliminating redundant API calls and ensuring data consistency.
- **Optimized API Usage:** The API client (`MerakiAPIClient`) leverages concurrent API calls using `asyncio.gather` to reduce latency and improve responsiveness.
- **Efficient State Management:** The `MerakiDataCoordinator` creates lookup tables for devices, networks, and SSIDs after each data fetch. This provides entities with fast, O(1) access to their data, avoiding slow, iterative lookups.
- **Modular Design:** The codebase is broken down into smaller, more focused modules. The API client uses a facade pattern, delegating calls to endpoint-specific handlers. Utility functions and sensor setup logic have also been modularized.

## 2. Core Components

<<<<<<< HEAD
\*\*2.1. `MerakiDataCoordinator`
=======
### 2.1. `MerakiDataCoordinator`
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

The heart of the integration is the `MerakiDataCoordinator`, located in `custom_components/meraki_ha/core/coordinators/meraki_data_coordinator.py`.

- **Responsibilities:**
  - Manages a single, periodic refresh of all data from the Meraki API via the `MerakiAPIClient`.
  - Holds the complete state of the integration in its `data` attribute.
  - After fetching data, it creates several lookup tables for efficient data retrieval by entities:
    - `devices_by_serial`: A dictionary mapping device serial numbers to device data.
    - `networks_by_id`: A dictionary mapping network IDs to network data.
    - `ssids_by_network_and_number`: A dictionary mapping a `(network_id, ssid_number)` tuple to SSID data.
- **Entity Interaction:** Entities in Home Assistant are subclasses of `CoordinatorEntity` and are linked to the `MerakiDataCoordinator`. They should not fetch their own data. Instead, they access the coordinator's `data` or use the efficient `get_device()`, `get_network()`, and `get_ssid()` methods to retrieve their state. When the coordinator updates its data, it notifies all listening entities, which then update their state via their `_handle_coordinator_update()` method.

<<<<<<< HEAD
\*\*2.2. `MerakiAPIClient`
=======
### 2.2. `MerakiAPIClient`
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

The `MerakiAPIClient`, located in `custom_components/meraki_ha/core/api/client.py`, is responsible for all communication with the Meraki Dashboard API.

- **Design:** It acts as a facade, providing a single entry point for fetching all data (`get_all_data`). It delegates the actual API calls to smaller, endpoint-specific handler classes located in `custom_components/meraki_ha/core/api/endpoints/`.
- **Concurrency:** The client uses `asyncio.gather` and a semaphore to fetch data from multiple API endpoints concurrently, significantly reducing the total time spent waiting for I/O. This makes the integration feel much more responsive, especially during startup.

<<<<<<< HEAD
\*\*2.3. Entity and Sensor Setup
=======
### 2.3. Entity and Sensor Setup
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- **`setup_helpers.py`:** The logic for creating all sensor entities is centralized in `custom_components/meraki_ha/sensor/setup_helpers.py`. This file was refactored from a single large function into several smaller, more manageable helper functions, each responsible for a specific category of sensor (e.g., `_setup_device_sensors`, `_setup_network_sensors`).
- **`sensor_registry.py`:** To ensure type safety and avoid `mypy` errors, the integration uses a sensor registry (`custom_components/meraki_ha/sensor_registry.py`). This registry explicitly defines which sensor classes should be created for each Meraki device type and what their constructor arguments are. This avoids the need for dynamic, untyped introspection.

## 3. Error Handling and Resiliency

The integration is designed to be resilient to transient API errors and network issues, providing a stable user experience.

<<<<<<< HEAD
\*\*3.1. Stale Data on Failure

If the `MerakiDataCoordinator` fails to fetch an update from the Meraki API, it does not immediately mark all entities as unavailable. Instead, it checks the timestamp of the last successful update. If the last successful data is within a configurable threshold (defaulting to 30 minutes), the coordinator will log a warning but continue to provide the existing "stale" data to all entities. This makes the integration resilient to brief network or API outages, preventing the user's dashboard from going blank due to a temporary glitch. This feature can be configured in the integration's options.

\*\*3.2. Partial Data Merging

The `MerakiAPIClient` fetches data from multiple endpoints concurrently. If one of these sub-requests fails, the integration does not discard all the data from the successful requests. Instead, it will use the data from the last successful coordinator run for the specific slice of data that failed. For example, if fetching VLAN information fails but device statuses succeed, the VLAN sensors will continue to show their previous state, while the device status sensors will show the latest information. This prevents a single, non-critical API failure from causing an entire category of sensors to become unavailable.

\*\*3.3. Persistent Caching
=======
### 3.1. Stale Data on Failure

If the `MerakiDataCoordinator` fails to fetch an update from the Meraki API, it does not immediately mark all entities as unavailable. Instead, it checks the timestamp of the last successful update. If the last successful data is within a configurable threshold (defaulting to 30 minutes), the coordinator will log a warning but continue to provide the existing "stale" data to all entities. This makes the integration resilient to brief network or API outages, preventing the user's dashboard from going blank due to a temporary glitch. This feature can be configured in the integration's options.

### 3.2. Partial Data Merging

The `MerakiAPIClient` fetches data from multiple endpoints concurrently. If one of these sub-requests fails, the integration does not discard all the data from the successful requests. Instead, it will use the data from the last successful coordinator run for the specific slice of data that failed. For example, if fetching VLAN information fails but device statuses succeed, the VLAN sensors will continue to show their previous state, while the device status sensors will show the latest information. This prevents a single, non-critical API failure from causing an entire category of sensors to become unavailable.

### 3.3. Persistent Caching
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

To improve startup times for Home Assistant, the integration uses a persistent disk cache (`diskcache`). The results of the `get_all_data` API call are cached on disk with a short TTL (2 minutes). When Home Assistant restarts, the integration can load the cached data almost instantly, making entities available right away while a fresh API call is made in the background.

## 4. Webhook Implementation Status

The integration now has a functional webhook implementation for real-time updates. The system can register a webhook with the Meraki API and handle incoming alerts. Currently, it processes alerts for "APs went down" and "Client connectivity changed" to provide near real-time status updates for device and client entities. The framework is in place to easily add handlers for more alert types in the future.
