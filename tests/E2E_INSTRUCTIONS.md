# End-to-End (E2E) Test Implementation Instructions

This document outlines the plan for expanding the E2E test suite for the Meraki Home Assistant integration. The goal is to verify the functionality of the custom frontend panel (`meraki-panel`) using Playwright.

## Current State
*   **Existing Test:** `tests/test_e2e_web_ui.py` currently checks if the frontend loads and displays the expected title.
*   **Method:** It spins up a local HTTP server to serve the build artifacts (`custom_components/meraki_ha/www/`) and uses Playwright to render the page with mocked `hass` and `panel` objects.

## Implementation Plan

Please implement the following test scenarios in `tests/test_e2e_web_ui.py` (or a new test file).

### Prerequisites
*   Ensure `playwright` is installed (`pip install playwright`).
*   Ensure the frontend is built (`cd custom_components/meraki_ha/www && npm install && npm run build`).

### Test Scenarios

#### 1. Navigation & Data Loading
*   **Scenario:** Verify that the dashboard loads the list of Networks from the mock data.
*   **Action:** Wait for `.network-card` elements to appear.
*   **Assertion:** Check that the number of network cards matches the mock data (e.g., 2 networks).

#### 2. Device Expansion
*   **Scenario:** User clicks on a Network card to view devices.
*   **Action:** Click on a `.network-card` (or the specific expand button).
*   **Assertion:** Verify that the "Cameras", "Switches", or "Wireless" sections become visible.

#### 3. Switch Port Control
*   **Scenario:** Toggle a switch port.
*   **Action:**
    *   Expand a Switch device.
    *   Locate a port toggle (e.g., `ha-switch` or standard checkbox).
    *   Click the toggle.
*   **Verification:**
    *   Ensure the UI state updates (optimistically).
    *   **Critical:** Verify that the `hass.callWS` mock received the correct message (service call to `meraki_ha.cycle_port` or similar).

#### 4. SSID Toggle
*   **Scenario:** Enable/Disable an SSID.
*   **Action:** Click the toggle for an SSID.
*   **Verification:** Verify `hass.callWS` call payload includes the correct `ssid_number` and `enabled` state.

#### 5. Camera Visibility
*   **Scenario:** Verify camera status indicator.
*   **Action:** Check the class/color of the camera icon/text (Green for online, Red for offline).

### Technical Notes
*   **Mocking:** You will need to expand the `hass` mock object in the HTML injection script. Ensure `hass.callWS` returns a Promise that resolves successfully.
*   **Selectors:** Use robust selectors (e.g., `data-testid` if available, or stable class names). If needed, add `data-testid` attributes to the React components (`StatusCard.tsx`, `DeviceTable.tsx`).
*   **Wait States:** The UI might have loading states. Use `page.wait_for_selector` to ensure elements are ready before interaction.
