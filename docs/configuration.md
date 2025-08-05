# Configuration

This page details the configuration options and setup instructions for the Meraki Home Assistant Integration.

## Obtaining Meraki API Credentials

To use this integration, you will need a Meraki API key and your Organization ID.

1.  **Log in to the Meraki Dashboard:** Go to [https://dashboard.meraki.com/](https://dashboard.meraki.com/).
2.  **Enable API Access:**
    *   Navigate to **Organization** > **Settings**.
    *   Under the **Dashboard API access** section, ensure API access is enabled.
3.  **Generate API Key:**
    *   Go to your **Profile** (click your name/email in the top right) > **My profile**.
    *   Scroll down to the **API access** section.
    *   Click **Generate new API key**.
    *   **Important:** Copy the generated API key and store it securely. You will not be able to see it again after navigating away from this page.
4.  **Find Organization ID:**
    *   The Organization ID is not directly visible in an obvious "Org ID" field.
    *   One way to find it is to look at the URL when you are viewing your organization dashboard. It might be part of the URL structure (e.g., `nXX...`).
    *   Alternatively, you can often find it by making a simple API call (e.g., using `curl` or Postman) to the `/organizations` endpoint with your API key. The response will list your accessible organizations and their IDs.

    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' 'https://api.meraki.com/api/v1/organizations'
    ```

## Setting up the Integration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" and select it.
4.  Follow the on-screen prompts to enter your API Key and Organization ID.

## Configuration Options

The following options can be configured when you first set up the integration, or at any time by navigating to the integration's card in **Settings -> Devices & Services** and clicking **Configure**.

*   **How many seconds between Meraki API refreshes:** How often (in seconds) to poll the Meraki API for updates. Default: 300. A shorter interval means more responsive sensors but significantly increases API calls to Meraki Cloud and may lead to rate limiting.
*   **Where would you like the Meraki device type in the name?:** Choose how device names are presented. 'Prefix' adds the Meraki device name before the entity name, 'Suffix' adds it after, 'Omitted' uses only the entity name.
*   **Auto-enable RTSP camera streams:** If checked, the integration will automatically enable the RTSP stream for all cameras that support it. This is useful for getting camera streams working without manual configuration in the Meraki dashboard.
*   **Use LAN IP for RTSP stream:** If checked, the integration will use the camera's LAN IP address for the RTSP stream. This is more efficient, but requires that Home Assistant is on the same network as the camera. If unchecked, the public IP address will be used.
*   **Webhook URL (optional):** A custom URL for Meraki webhooks. If left blank, the integration will use the default Home Assistant webhook URL.
