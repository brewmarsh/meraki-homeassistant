### AI Agent Instructions

Your task is to refactor the Meraki MV camera integration to properly handle various camera models and their unique features. This requires a **granular, type-aware approach** that goes beyond basic video streams. The goal is to dynamically expose all supported sensors and controls for each specific camera model.

1.  **Refactor `MerakiRepository` for Camera-Specific Endpoints**: Identify and implement the necessary API endpoints to retrieve a camera's specific capabilities. This may include endpoints for `getDeviceCameraAnalyticsOverview`, `getDeviceCameraAnalyticsZones`, and `getDeviceCameraVideoLink`.
2.  **Modularize Camera-Specific Logic**: Create a new, dedicated `CameraService` to handle all camera-related functions. This service will use the repository to fetch data and expose methods that are agnostic of the camera model, while the underlying logic handles the model-specific differences.
3.  **Implement a Type-Aware `MVHandler`**: The `MVHandler` must be refactored to be model-aware. During discovery, it should query the device for its model type and then conditionally create entities based on that model's supported features.
4.  **Enforce Strict Code Separation**: As instructed previously, break down complex logic into small, single-purpose functions. No file should exceed 300 lines, and indentation should be limited to a maximum of three levels.

---

### Camera Entity Requirements

To ensure a consistent and feature-rich experience, all Meraki camera devices must have the following entities created by the `MVHandler`.

- **`MerakiCamera`**: The main `camera` entity that displays the RTSP video stream.
- **`MerakiMotionSensor`**: A `binary_sensor` that indicates motion.
- **`MerakiSnapshotButton`**: A `button` entity to trigger a snapshot.
- **`MerakiRtspUrlSensor`**: A `sensor` that displays the current RTSP stream URL.
- **`RTSPStreamSwitch`**: A `switch` entity to enable or disable the RTSP stream.
- **`AnalyticsSwitch`**: A `switch` entity to enable or disable camera analytics.

**Conditional Entities:**

- **`MerakiPersonCountSensor`**: A `sensor` for the person count, created only if the camera model supports person detection.
- **`MerakiVehicleCountSensor`**: A `sensor` for the vehicle count, created only if the camera model supports vehicle detection.

**Important Implementation Details:**

- All camera-related entities must have a `device_info` property that correctly links them to the parent Meraki camera device in Home Assistant.
- The on/off control for the RTSP stream must be handled by the `RTSPStreamSwitch` entity, not by methods on the `MerakiCamera` entity itself.

---

### Refactor Plan for Meraki MV Cameras

This plan builds on the existing architecture to implement a dynamic and feature-rich integration for Meraki MV cameras, properly handling the unique capabilities of each model.

#### Phase 1: API and Repository Updates

1.  **Enhance `MerakiApiClient`**:
    - Add new methods to retrieve **camera analytics data** (`get_device_camera_analytics`, `get_network_camera_analytics_history`). These endpoints allow access to rich data like object counts (people/vehicles) and motion history.
    - Add a method to get **live video stream URLs** (`get_device_camera_video_link`), which is the correct way to get the RTSP stream.

2.  **Add `CameraRepository` Methods**:
    - Create a new `CameraRepository` or expand the existing `MerakiRepository` to include camera-specific methods. This repository layer will abstract the different API calls based on a camera's model and capabilities.
    - Methods should include `get_camera_features(serial)` to retrieve a camera's model-specific capabilities, `get_analytics_data(serial)` to fetch object detection and motion data, and `get_video_url(serial)` for the stream.

#### Phase 2: Create a Dedicated Camera Service

1.  **Develop `CameraService` (`meraki_ha/services/camera_service.py`)**:
    - This new service will be injected with the `MerakiRepository`.
    - It will contain methods like `get_supported_analytics(serial)` that query the repository and return a list of features (e.g., `["person_detection", "vehicle_detection"]`).
    - Other methods will retrieve the actual analytics data and the video stream URL. The `CameraService`'s job is to shield the handlers from the complexities of the repository's API calls.

#### Phase 3: Dynamic Entity Creation with `MVHandler`

1.  **Refactor `MVHandler`**:
    - Update the `MVHandler` to be **type-aware**. When it's created, it should get the device's model and query the `CameraService` for supported features.
    - The handler will then **conditionally create** Home Assistant entities based on the returned feature list.
      - **Camera Entity**: Always create a base camera entity for the video stream. The stream URL will come from the `CameraService`.
      - **Sensor Entities**: If the `CameraService` reports "person_detection" is supported, create a `person_count` sensor. If it supports "vehicle_detection," create a `vehicle_count` sensor.
      - **Binary Sensor Entities**: Create motion detection binary sensors based on motion history data from the `CameraService`.
      - **Button Entities**: For models that support snapshots, create a "Take Snapshot" button that calls the snapshot API endpoint via the `CameraService`.

2.  **Update `config_flow`**:
    - Ensure the `CameraService` is instantiated and injected into the `MVHandler`.

#### Phase 4: Testing and Cleanup

1.  **Create Model-Specific Mock Data**: When testing, use mock API responses that represent different camera models (e.g., one mock for an MV12, another for an MV93 with 360° view and analytics). This will allow you to test that the `MVHandler` correctly creates the right entities for each model.
2.  **Remove Legacy Code**: Delete any old code that handles MV cameras in a monolithic or non-modular way, ensuring all new logic is routed through the repository and the new `CameraService`.
