# Camera Requirements

This document outlines the functional requirements for camera entities in the Meraki Home Assistant integration.

## RTSP Stream URL Handling

The integration must provide a reliable RTSP stream URL for camera entities. The logic for determining this URL should follow a specific priority and fallback mechanism to ensure maximum reliability and user control.

### R6: RTSP URL Logic

The `stream_source` property of the `MerakiCamera` entity must implement the following logic:

1.  **Check `use_lan_ip` Setting:** The primary factor determining the URL is the `use_lan_ip` option in the integration's configuration.

2.  **If `use_lan_ip` is `True`:**
    - **Priority 1: Local API URL:** Check if the RTSP URL provided by the Meraki API (`rtspUrl` from the video settings endpoint) is already a local IP address (i.e., it falls within a reserved private IP range like `192.168.0.0/16`, `10.0.0.0/8`, or `172.16.0.0/12`). If it is, use this URL.
    - **Priority 2: Construct Local URL:** If the API-provided URL is not a local IP, attempt to construct a valid RTSP URL using the camera's `lanIp` property.
    - **Fallback: Public API URL:** If the `lanIp` is not available, fall back to using the public URL provided by the API as a last resort.

3.  **If `use_lan_ip` is `False` (Default):**
    - **Priority 1: Public API URL:** Prioritize using the RTSP URL provided by the Meraki API.
    - **Fallback: Construct Local URL:** If the URL from the API is missing, invalid (e.g., not a valid RTSP format), or unavailable, fall back to constructing a local URL using the camera's `lanIp` property.

4.  **Validation:** In all cases, before returning a URL, the integration must validate that it is a properly formatted RTSP URL (i.e., starts with `rtsp://`). If no valid URL can be found or constructed, the stream source should be `None`.
