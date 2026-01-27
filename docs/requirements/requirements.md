# Requirements Verification (ha-camera-refactor2)

This document verifies the state of the codebase against the requirements for the camera refactoring task.

- **R1: Complete Discovery:**

  - **[VERIFIED]** `MVHandler` discovers and creates the `MerakiCamera` entity.
  - **[VERIFIED]** `MVHandler` correctly passes `config_entry` and `CameraService` to the `MerakiCamera` entity during initialization.

- **R2: RTSP Stream Control:**

  - **[FAIL]** The `MerakiCamera` entity is missing the `turn_on` and `turn_off` methods required for stream control.
  - **[VERIFIED]** The `CameraService` has the necessary `async_set_rtsp_stream_enabled` method to control the stream.

- **R3: Configuration Honored:**

  - **[FAIL]** The `MVHandler` does not currently check the `rtsp_stream_enabled` option at startup to proactively enable the stream.

- **R4: API Robustness:**

  - **[FAIL]** The `core/utils/api_utils.py` module's `validate_response` function raises an exception on empty API responses, causing crashes instead of handling them gracefully. This is the source of the "Empty response from API" error.

- **R5: Informative Feedback:**
  - **[PARTIAL]** The `MerakiCamera` entity has some error handling for streams, but it needs to be improved to be more state-driven and provide clearer feedback through the coordinator. The `camera_repository.py` also needs to be improved to handle non-RTSP URLs.

This verification confirms the need for the planned refactoring steps. The new requirements (R4, R5) are now considered part of the standard for this integration.
