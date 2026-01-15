# Configuration

## Obtaining Meraki API Credentials

To use this integration, you will need a Meraki API key and your Organization ID.

1.  **Log in to the Meraki Dashboard:** Go to [https://dashboard.meraki.com/](https://dashboard.meraki.com/).
2.  **Enable API Access:**
    - Navigate to **Organization** > **Settings**.
    - Under the **Dashboard API access** section, ensure API access is enabled.
3.  **Generate API Key:**
    - Go to your **Profile** (click your name/email in the top right) > **My profile**.
    - Scroll down to the **API access** section.
    - Click **Generate new API key**.
    - **Important:** Copy the generated API key and store it securely. You will not be able to see it again after navigating away from this page.
4.  **Find Organization ID:**
    - **Easiest Method:** The Organization ID is displayed at the bottom of every page in the Meraki dashboard.
    - **Alternative Method (API):** You can find it by making a simple API call to the `/organizations` endpoint with your API key.

    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' '[https://api.meraki.com/api/v1/organizations](https://api.meraki.com/api/v1/organizations)'
    ```

## Setting up the Integration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" and select it.
4.  Follow the on-screen prompts to enter your API Key and Organization ID.

## Configuration Options

The following options can be configured when you first set up the integration, or at any time by navigating to the integration's card in **Settings -> Devices & Services** and clicking **Configure**.

-   **Scan Interval:** How often (in seconds) to poll the Meraki API for updates. Default: 300.
-   **Enable Device Tracker:** Whether to enable the device tracker entity for clients. Default: true.
-   **Enable VLAN Management:** Whether to enable VLAN management entities. Default: false.
-   **Ignored Networks:** A comma-separated list of network IDs to ignore.
