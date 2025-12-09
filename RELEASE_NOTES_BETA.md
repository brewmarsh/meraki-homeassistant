# Meraki HA Beta Release Notes (v2.2.x)

This beta release cycle has focused on expanding hardware support (MT40), refining the custom frontend panel, and improving project stability.

## 🚀 New Features

*   **MT40 Smart Power Controller:** Added dedicated support for the MT40 sensor, allowing for power monitoring and control directly from Home Assistant.
*   **Frontend Panel Improvements:**
    *   **SSID Layout:** Completely redesigned the SSID section for better readability.
    *   **Device Grouping:** Improved how devices are categorized (Wireless, Switching, Cameras, Sensors).
    *   **VLAN Support:** Added visibility for VLAN configurations in the panel.
    *   **Icons:** Added missing icons for various device types.

## 🐛 Bug Fixes

*   **Camera Status:** Fixed an issue where cameras would incorrectly report their online/offline status or client counts.
*   **UI Layout:** Resolved an overlap issue in the SSID panel layout.
*   **Dependencies:** Resolved multiple dependency conflicts (pytest, homeassistant) and addressed security vulnerabilities (uv).

## 🔧 Under the Hood

*   **Code Quality:** Major cleanup of linting errors and formatting updates using `ruff`.
*   **Testing:** Improved E2E test reliability and CI pipeline stability.
*   **Python 3.13:** Added compatibility updates for Python 3.13.

---
**Testing Instructions:**
Check the new SSID layout in the Meraki Panel and ensure MT40 sensors allow control as expected.
