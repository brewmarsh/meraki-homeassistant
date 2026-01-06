# Meraki HA Beta Release Notes (v2.2.1-beta.1)

This release focuses on camera improvements, API error handling, and performance optimizations.

## 🚀 New Features

### Camera Enhancements
*   **Snapshot Refresh Interval:** Configurable auto-refresh for camera snapshots on the dashboard. Set interval in seconds (0 = on-demand only). Cached snapshots reduce API calls and load instantly.
*   **Cloud Video URL Attribute:** Camera entities now expose a `cloud_video_url` attribute that opens the Meraki Dashboard video viewer in a browser.
*   **Web Panel Camera View:** Enhanced camera device view with live snapshots and "Open in Meraki Dashboard" button for cloud video access (works even when RTSP is unavailable or in use).
*   **Link to External NVR Cameras:** Connect Meraki cameras to other camera entities (e.g., Blue Iris). Perfect for setups where RTSP goes to an NVR first. Configure via the "Link Camera" button in the web panel.

### API & Performance
*   **Network Filtering:** Integration now only polls networks enabled in settings, reducing unnecessary API calls and improving performance for large deployments.
*   **Web API Stream Source:** WebSocket endpoint for camera stream URL accepts optional `stream_source` parameter ("rtsp" for direct streaming, "cloud" for Dashboard viewing).

### Frontend Panel
*   **HA Custom Panel Architecture:** Refactored to use proper Home Assistant panel integration with `hass.callWS()` for authenticated API calls.
*   **Redesigned UI:** New card-based layout with CSS variables for light/dark theme support, device status badges, and model-specific icons.
*   **Network Filtering:** Panel only displays enabled networks with auto-expand for single network setups.

## 🐛 Bug Fixes

*   **"Invalid device type" Error:** Fixed API error occurring 1,900+ times by filtering networks to only query client-capable types (wireless, appliance, switch, cellularGateway). Camera-only networks no longer cause 400 Bad Request errors.
*   **Camera Snapshot Failures:** Added retry mechanism (3 attempts with 2-second delays) for snapshot generation. Gracefully handles 202/400 responses and falls back to cached snapshots.
*   **Camera Stream Errors:** Fixed "Error opening stream" when using cloud video URLs. Meraki cloud links are Dashboard pages (not direct video streams), so streaming now correctly uses RTSP only. Cloud URL is exposed as an attribute for browser viewing.
*   **Traffic Analysis Logging:** Informational errors (traffic analysis disabled, VLANs disabled) no longer logged at ERROR level, reducing log noise.
*   **Frontend Click Handling:** Fixed click handling for device rows and entity links.
*   **WebSocket Registration:** Fixed `async_setup_websocket_api` registration for subscription handler.

## 🔧 Under the Hood

*   **Code Quality:** Continued cleanup of linting errors and formatting updates using `ruff`.
*   **Error Handling:** Improved error propagation for informational API errors.
*   **Snapshot Caching:** Implemented in-memory caching with configurable TTL.

---

**Configuration Options (Settings → Devices & Services → Meraki HA → Configure):**
*   **Camera Snapshot Refresh Interval:** 0-3600 seconds (0 = on-demand only)

**Important Note on Camera Streaming:**
*   Camera streaming in Home Assistant uses **RTSP only** (requires enabling RTSP server in Meraki Dashboard)
*   The cloud video URL from Meraki is a Dashboard web page, not a direct video stream
*   For cameras that don't support RTSP (e.g., MV2), view the video via the `cloud_video_url` attribute in a browser

**Testing Instructions:**
1. Set snapshot interval to 30-60 seconds and verify auto-refresh on dashboard
2. Confirm API errors in logs have significantly decreased
3. Verify only enabled networks are polled (check debug logs)
4. For cameras with RTSP enabled, confirm video streaming works
5. Check camera entity attributes for `cloud_video_url` to open Dashboard viewer
6. In web panel, click on a camera device and test:
   - "Refresh Snapshot" button loads a fresh image
   - "Open in Meraki Dashboard" button opens cloud video in new browser tab
7. Test camera linking feature:
   - Click "Link Camera" button on a Meraki camera device
   - Select a Blue Iris or other camera entity from the dropdown
   - Click "Save" and switch to "Linked Camera" tab to view the stream
   - Check camera entity attributes for `linked_camera_entity`
