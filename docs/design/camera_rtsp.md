# Design: RTSP Stream Handling for Cameras

This document details the technical design and architecture for managing RTSP streams on Meraki cameras within the Home Assistant integration. The design prioritizes a centralized, coordinator-driven approach to ensure data consistency, efficiency, and a responsive user experience.

## 1. Core Principles

- **Single Source of Truth:** The `MerakiDataUpdateCoordinator` is the single source of truth for all device states, including camera video settings. All related entities (camera, sensor, switch) must derive their state from the coordinator.
- **Optimistic UI:** Configuration entities, such as the RTSP switch, must use the "Optimistic UI with Cooldown" pattern to provide immediate feedback to the user while gracefully handling the Meraki API's provisioning delay.
- **Efficiency:** Redundant API calls are avoided. Entities do not make their own `GET` requests; they rely on the coordinator's scheduled refresh. Actions (e.g., turning a switch on/off) are dispatched through a dedicated service.

## 2. Component Breakdown

### 2.1. `MerakiDataUpdateCoordinator`
- **Responsibility:** Fetches all device data, including camera details and their `video_settings`, at a regular interval. It holds the authoritative state.

### 2.2. `CameraService`
- **Responsibility:** Acts as a centralized service for all camera-related actions. It encapsulates the business logic for making API calls that modify state.
- **`async_set_rtsp_stream_enabled(serial, enabled)`:** This method is the single point of contact for enabling or disabling the RTSP stream for a camera. It makes the `PUT` request to the Meraki API.

### 2.3. `MerakiCamera` Entity (`camera.py`)
- **Inheritance:** `CoordinatorEntity`
- **State:** Derives its `is_streaming` status directly from the `rtspServerEnabled` flag in the coordinator's data for the corresponding device.
- **`stream_source`:**
    - Implements the logic to construct the RTSP URL, prioritizing the local `lanIp` before falling back to the cloud-provided `rtspUrl`.
- **`async_turn_on`/`async_turn_off`:**
    - Implements the optimistic UI pattern.
    - It immediately updates its own state, calls the `CameraService` to dispatch the API call, and registers a cooldown with the coordinator.

### 2.4. `RTSPStreamSwitch` Entity (`switch/camera_controls.py`)
- **Inheritance:** `CoordinatorEntity`, `SwitchEntity`
- **State (`is_on`):** Derived directly from the `rtspServerEnabled` flag in the coordinator's data.
- **`async_turn_on`/`async_turn_off`:**
    - Implements the optimistic UI pattern.
    - It writes its optimistic state to Home Assistant.
    - It calls `CameraService.async_set_rtsp_stream_enabled` to perform the action.
    - It registers a cooldown with the coordinator using `coordinator.register_pending_update(self.unique_id)`.
- **`_handle_coordinator_update`:** Ignores data updates from the coordinator while a cooldown is active for its `unique_id`.

### 2.5. `MerakiRtspUrlSensor` Entity (`sensor/device/rtsp_url.py`)
- **Inheritance:** `CoordinatorEntity`, `SensorEntity`
- **State:**
    - If `rtspServerEnabled` is `True`, its state is the RTSP URL (constructed with the same logic as the camera's `stream_source`).
    - If `rtspServerEnabled` is `False`, its state is the string "Disabled".
- **Efficiency:** It has no `async_update` method and makes no API calls. Its state is computed based on data received from the coordinator.

## 3. Startup Logic (`__init__.py`)

- The `async_setup_entry` function orchestrates the setup.
- **"Auto RTSP" Feature:**
    - After the initial coordinator refresh, it checks if `CONF_AUTO_RTSP` is enabled.
    - If `True`, it iterates through all camera devices (excluding unsupported models like MV2).
    - It creates a list of `asyncio` tasks, with each task being a call to `CameraService.async_set_rtsp_stream_enabled(serial, True)`.
    - It uses `asyncio.gather` to execute all API calls concurrently, ensuring a fast startup.