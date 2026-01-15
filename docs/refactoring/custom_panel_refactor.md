# Requirements: Meraki Dashboard Refactor & Dual-Compatibility (v2026.1)

## 1. Objective

Refactor the custom Meraki panel into a native Home Assistant Dashboard utilizing the **Sections view** layout. This ensures full compatibility with 2026.1 navigation while providing a graceful **Dual-Registration** fallback for older versions.

## 2. Technical Specifications

### A. Framework & Framework Migration

* **Target Framework:** Migrate all custom frontend components from legacy HTML/JS to **Lit 3.x**.
* **Grid Intelligence:** Components must implement `getGridOptions()` to support the native 2026.1 drag-and-drop grid.
* **Styling:** Utilize CSS variables (e.g., `--ha-card-background`, `--primary-text-color`) for automatic theme adaptation.

### B. Navigation & Dual-Registration

The backend (`__init__.py`) must detect the Home Assistant version to choose the registration method:

* **v2026.1 or Newer:**
* Register a **Lovelace Dashboard** via `frontend.async_register_built_in_panel`.
* **Dashboard Config:** Set `view_type: "sections"` and include a default `ui-lovelace.yaml` layout.


* **Older Versions:**
* Fall back to `panel_custom` registration to maintain existing sidebar functionality and bookmarks.


* **Common Settings:** Icon: `mdi:lan-check`, `require_admin: false`.

### C. Layout Architecture (Sections View)

The dashboard will implement a three-tier priority grid:

1. **Connectivity Summary (Header):**
* **Version String:** Display the integration version (e.g., "2.0.0-beta.69") prominently.
* **Live Status:** A connectivity chip for Meraki Cloud health.


2. **Security & Surveillance:**
* WebRTC camera feeds using optimized 2026.1 "Picture Glance" or "Sub-view" cards.


3. **Network Controls:**
* Grouped SSID toggles and PoE switch management sections.



## 3. Data Flow & State Management

* **WebSocket API:** Implement a new command `meraki_ha/get_version` to allow the Lit components to fetch the version string regardless of the registration method.
* **Throttling:** Apply a 500ms debounce to all network-wide toggles to prevent API rate-limiting.
* **Interaction:** Ensure clicking any card opens the native **More Info** dialog for full device details (IP, MAC, history).

## 4. Implementation Steps for Jules

1. **Phase 1 (Backend):** Implement version-checking logic in `__init__.py` and the new WebSocket command.
2. **Phase 2 (Frontend):** Convert existing views into **Lit 3.x** components with grid support.
3. **Phase 3 (Configuration):** Draft the default `ui-lovelace.yaml` Sections layout.
4. **Phase 4 (Validation):** Deploy to the **Smoke Test Server** and verify:
* Version "2.0.0-beta.69" is displayed via WebSocket.
* The dashboard scales and flows correctly on the 2026.1 mobile view.
