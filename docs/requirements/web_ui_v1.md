# Web-Based Configuration UI Requirements

This document outlines the requirements for a standalone web-based user interface (UI) to configure the `meraki_ha` Home Assistant integration. The UI should be a single-page application and should run on a web server started by the integration itself.

---

## 1. General Requirements

- **Technology Stack:** The UI will be a standalone single-page application using HTML, CSS, and JavaScript. It must not rely on any heavy front-end frameworks (e.g., React, Vue.js).
- **Web Server:** The integration's back-end component will provide a lightweight web server (e.g., using `aiohttp`) to serve the UI files and handle API requests.
- **User Flow:** The user will navigate to a specific URL (e.g., `http://<ha_ip>:<ha_port>/meraki_ha_config`) to access the UI.
- **Communication:** The UI will communicate with the back-end web server via a REST API to save and retrieve configuration data.

---

## 2. UI/UX Requirements

- **Single-Page Layout:** The UI should be contained within a single HTML page.
- **Responsive Design:** The UI must be responsive and usable on both desktop and mobile browsers.
- **Branding:** The UI should have a clean, modern design that is visually consistent with the Home Assistant aesthetic, though it doesn't need to be an exact replica.
- **Form Validation:** The UI must perform client-side validation on all input fields to ensure data is in the correct format before submission.
- **User Feedback:** The UI must provide clear and concise feedback to the user upon submission, indicating whether the configuration was saved successfully or if there were errors. This feedback should be non-intrusive (e.g., a temporary banner or message).

---

## 3. Functional Requirements

- **Configuration Form:** The UI must display a form containing the configuration items. The specific fields will be provided separately.
- **Save Functionality:** There must be a "Save" button that, when clicked, collects all the form data and sends it to the back-end API.
- **API Endpoints:** The back-end web server must expose two API endpoints:
- `GET /api/config`: This endpoint should retrieve the current saved configuration data and return it as a JSON object. The UI should use this to pre-populate the form fields on page load.
- `POST /api/config`: This endpoint should accept a JSON payload containing the new configuration data. Upon successful processing, it should return a success message. If there's an error (e.g., invalid data), it should return an error message with a clear description.
- **Error Handling:** The UI must gracefully handle API errors. If the back-end returns an error, the UI should display the error message to the user.
- **Confirmation:** After a successful save, the UI should display a confirmation message and potentially offer a link to return to the main Home Assistant dashboard.
