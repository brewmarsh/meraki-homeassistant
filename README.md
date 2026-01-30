# Meraki Home Assistant Integration 🏠☁️

[![Current Version](https://img.shields.io/github/v/release/brewmarsh/meraki-homeassistant?include_prereleases&label=Current%20Version)](https://github.com/brewmarsh/meraki-homeassistant/releases)
[![Pull Request Validation](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/pull-request.yaml/badge.svg)](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/pull-request.yaml)
[![Hassfest Validation](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/hassfest.yaml)
[![codecov](https://codecov.io/gh/brewmarsh/meraki-homeassistant/branch/main/graph/badge.svg)](https://codecov.io/gh/brewmarsh/meraki-homeassistant)
[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Welcome to the **Meraki Home Assistant Integration**! This project bridges the gap between your Cisco Meraki cloud-managed network and your local Home Assistant instance. Whether you're managing a home lab, a small business, or just love having total control over your network gear, this integration has you covered.

**Note:** This is currently in **Beta**. We're moving fast and improving stability, so feedback is always welcome!

## Table of contents

- [Key features](#key-features-✨)
- [Installation](#installation-🛠️)
- [Configuration](#configuration-⚙️)
- [Web UI](#web-ui-🖼️)
- [Services & controls](#services--controls-🛗️)
  - [Parental controls (client blocking)](#parental-controls-client-blocking)
  - [Content filtering](#content-filtering)
  - [SSID control](#ssid-control)
- [Entities](#entities-🧩)
  - [Device & entity model](#device--entity-model)
  - [Organization-wide sensors](#organization-wide-sensors)
  - [Camera entities & sensors](#camera-entities--sensors)
  - [Physical device sensors](#physical-device-sensors)
  - [Network sensors](#network-sensors)
  - [VLAN sensors](#vlan-sensors)
  - [Appliance port sensors](#appliance-port-sensors)
  - [SSID sensors](#ssid-sensors)
  - [Environmental sensors (MT series)](#environmental-sensors-mt-series)
- [Automation examples](#automation-examples-🚀)
- [Troubleshooting](#troubleshooting)
- [How to contribute](#how-to-contribute)
- [Known issues & limitations](#known-issues--limitations)
- [Disclaimer](#disclaimer)

## Screenshots 📸

|                                                     Network View                                                      |                                                     Device Detail View                                                      |
| :-------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: |
| ![Network View](https://user-images.githubusercontent.com/1099616/279869151-24702f37-646d-4176-963d-2103f6f3630d.png) | ![Device Detail View](https://user-images.githubusercontent.com/1099616/279869158-2947a195-5c02-4580-b7a4-315111956f46.png) |

## Key features ✨

- **Comprehensive Monitoring:** Keep tabs on all your Meraki hardware, including Wireless Access Points (MR/GR), Switches (MS/GS), Security Appliances (MX), Cameras (MV), and Environmental Sensors (MT).
- **Powerful Controls:** Enable/disable SSIDs, block specific clients (Parental Controls), and manage content filtering categories directly from Home Assistant.
- **Web Interface:** A dedicated web UI for advanced features like guest Wi-Fi management and viewing event logs.
- **Rich Sensor Data:** Creates a wide array of sensors for device status, client counts, data usage, firmware updates, PoE consumption, and much more.
- **Camera Integration:** View live RTSP streams from your Meraki cameras within Home Assistant.

## Troubleshooting

If you encounter issues with the integration, please check the following:

- **API Key and Organization ID:** Ensure that your API key and organization ID are correct.
- **API Access:** Make sure that API access is enabled in your Meraki dashboard.
- **Home Assistant Logs:** Check the Home Assistant logs for any error messages related to the integration.
- **Restart Home Assistant:** If you've made any changes to the integration's configuration, restart Home Assistant to apply them.

---

_Built with ❤️ by the Open Source Community._
