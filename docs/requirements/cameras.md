# Camera Requirements

This document outlines the functional requirements for camera entities in the Meraki Home Assistant integration, focusing on RTSP stream handling.

## R1: RTSP Stream Configuration

The integration provides robust controls for managing RTSP (Real-Time Streaming Protocol) on supported Meraki cameras.

### R1.1: Auto RTSP on Startup
- **Requirement:** The integration must include a configuration option, `CONF_AUTO_RTSP`, which is a boolean that defaults to `False`.
- **Behavior:** When this option is enabled (`True`), the integration shall automatically enable the RTSP stream for all supported camera devices every time Home Assistant starts up.
- **Exclusions:** Cameras that do not support RTSP (e.g., MV2 models) must be excluded from this process.

### R1.2: RTSP Enabled Switch
- **Requirement:** Each supported camera device must have an "RTSP Enabled" switch entity.
- **Behavior:**
    - This switch allows the user to manually enable or disable the RTSP stream for the camera.
    - The switch must use an optimistic UI pattern with a cooldown period to handle the provisioning delay of the Meraki API, providing a responsive user experience.
    - The state of the switch must reflect the `rtspServerEnabled` property from the camera's video settings.
    - At startup, if `CONF_AUTO_RTSP` is enabled, this switch shall be in the "On" state.

## R2: Camera and Sensor Entities

The state of the RTSP stream must be clearly represented across the camera and sensor entities.

### R2.1: Camera Entity (`camera`)
- **Requirement:** The primary camera entity must be coordinator-driven, sourcing its state from the central data coordinator.
- **Streaming Logic (`is_streaming`):** The camera is considered to be streaming if the `rtspServerEnabled` property is `True` and a valid stream source is available.
- **Stream Source (`stream_source`):**
    1.  **Priority 1: Local LAN IP:** The integration must prioritize constructing the RTSP URL using the camera's local LAN IP address (`lanIp`).
    2.  **Fallback: Cloud URL:** If the `lanIp` is not available, the integration shall fall back to using the cloud-provided RTSP URL (`rtspUrl`).
    3.  If neither is available, the stream source should be `None`.
- **Unsupported Cameras:** Cameras that do not support RTSP (e.g., MV2 models) must not support streaming features.

### R2.2: RTSP URL Sensor (`sensor`)
- **Requirement:** Each supported camera must have an "RTSP URL" sensor entity.
- **Behavior:**
    - This sensor must be coordinator-driven.
    - When the RTSP stream is enabled, the sensor's state must be the RTSP stream URL, following the same priority logic as the camera entity's `stream_source`.
    - When the RTSP stream is disabled, the sensor's state must be "Disabled".
- **Unsupported Cameras:** This sensor must not be created for cameras that do not support RTSP.