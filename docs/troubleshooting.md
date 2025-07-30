# Troubleshooting

This page provides common troubleshooting steps and solutions for issues encountered with the Meraki Home Assistant Integration.

## Common Issues

### Invalid Authentication

If you receive an "Invalid authentication" error, it means that your API key or Organization ID is incorrect. Please double-check your credentials and try again.

### Cannot Connect

If you receive a "Cannot connect" error, it means that Home Assistant is unable to connect to the Meraki API. Please check your internet connection and ensure that there are no firewalls blocking access to the Meraki API.

### API Rate Limits

The Meraki API has rate limits that restrict the number of API calls that can be made in a given time period. If you have a large number of devices or a short scan interval, you may exceed these rate limits. If this happens, you will see errors in the Home Assistant logs. To resolve this, you can increase the scan interval in the integration's options.

## Getting Help

If you are still having issues, you can get help in the following ways:

*   **Home Assistant Community Forums:** Post a question in the [Meraki integration thread](https://community.home-assistant.io/t/meraki-integration/12345) (link is a placeholder).
*   **GitHub Issues:** If you believe you have found a bug, please open an issue on the [GitHub repository](https://github.com/your-repo/meraki-ha).
