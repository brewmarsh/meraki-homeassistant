# Meraki HA Future Roadmap (Post v2.6.0)

This document outlines the remaining high-value features, Home Assistant Blueprints, and Custom Lovelace Cards for the Meraki integration.

## Blueprints (Pending Automations)

- **EV Arrived Trigger**
  - Use Meraki's presence detection (scanning radio or client connection) to trigger automation when an EV's MAC address is spotted.
  - Potential Actions: Open garage doors, turn on driveway lights, or send a greeting.
- **Dinner Time Policy Enforcer**
  - Automate the scheduling of Meraki Group Policies to restrict bandwidth or block specific categories/sites during designated family times.
  - Integration: Already supported via `select` entities, just needs the blueprint template.
- **Scheduled Guest Key**
  - Periodically auto-generate a new Guest Wi-Fi IPSK and notify service workers or temporary staff via mobile app, email, or SMS.
  - Integration: Uses the `meraki_ha.create_guest_key` service.
- **Dead Node Auto-Heal**
  - Monitor the availability of Home Assistant entities representing downstream devices. If an entity goes unavailable for a set period, cycle the corresponding Meraki switch port to attempt a hardware reboot.
- **MT Sensor Threshold Alerts**
  - Pre-configured critical notification templates for Meraki MT sensors (Temperature, Humidity, Water Leak, Door/Window).

## Custom Lovelace Cards (Pending Dashboards)

- **Event Host QR Generator**
  - A dedicated card for generating and displaying Guest Wi-Fi credentials with a scanable QR code.
  - Status: Core logic in frontend, needs standalone card packaging.
- **Client Locator Glance Card**
  - Quickly search for a connected client by name or MAC address.
  - Displays: Parent Access Point, current RSSI/Signal strength, and connection duration.
- **Network Vitals Header**
  - A compact header for dashboards showing high-level network health (Mini traffic graphs, Green/Yellow/Red status dots).

## Native HA Entity Integrations (Gaps)

- **Native Firmware Management**
  - Allow users to view and trigger Meraki network upgrades natively from the HA UI via the `update` entity.
- **PoE Power Cycling Service**
  - Add a dedicated service to perform a PoE power cycle on a switch port (differing from a simple enable/disable toggle).

## Completed Features (v2.6.0)

- [x] **Edge Analytics & Presence**: Feed MV camera object detection (person/vehicle) directly into HA binary sensors.
- [x] **Network Device Tracking**: High-reliability network-level presence tracking via MR access point associations.
- [x] **PoE Port Control**: Expose MS switch ports as native toggles.
- [x] **Dynamic Bandwidth Toggles**: Support for toggling SSIDs and selecting Group Policies via native entities.
- [x] **Secure Diagnostics**: Comprehensive PII redaction for organization and device data.
- [x] **Reliable Management Controls**: Hardened client blocking and SSID toggling with verification.
