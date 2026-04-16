# Meraki HA Future Roadmap (Post v2.6.0)

This document outlines the remaining high-value features and native entity gaps for the Meraki integration.

## Native HA Entity Integrations (Remaining Gaps)

- **Native Firmware Management**
  - Allow users to view and trigger Meraki network upgrades natively from the HA UI via the `update` entity.
- **PoE Power Cycling Service**
  - Add a dedicated service to perform a PoE power cycle on a switch port (differing from a simple enable/disable toggle).
- **MT Sensor Threshold Alerts (Blueprint Expansion)**
  - Expand existing blueprints to include pre-configured notification templates for MT sensors (Temperature, Humidity, Water Leak).

## Completed Features (v2.6.0)

- [x] **Blueprints**: WAN Failover Alerts, Guest Wi-Fi Creation, and Scheduled Content Filtering are all implemented.
- [x] **Custom Lovelace Cards**: Guest Access, Network Vitals, VLAN, Content Filtering, and Wi-Fi QR cards are all implemented in the `frontend/` package.
- [x] **Edge Analytics & Presence**: MV camera object detection (person/vehicle) feeds directly into HA binary sensors.
- [x] **Network Device Tracking**: High-reliability presence tracking via MR access point associations.
- [x] **PoE Port Control**: Expose MS switch ports as native toggles.
- [x] **Dynamic Bandwidth Toggles**: Support for toggling SSIDs and selecting Group Policies via native entities.
- [x] **Secure Diagnostics**: Comprehensive PII redaction for organization and device data.
- [x] **Reliable Management Controls**: Hardened client blocking and SSID toggling with verification.
