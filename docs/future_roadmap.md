# Meraki HA Future Roadmap

This document outlines the planned high-value Home Assistant Blueprints and Custom Lovelace Cards for the Meraki integration.

## Blueprints (Automations)

- **EV Arrived Trigger**
  - Use Meraki's presence detection (scanning radio or client connection) to trigger automation when an EV's MAC address is spotted.
  - Potential Actions: Open garage doors, turn on driveway lights, or send a greeting.
- **Dinner Time Policy Enforcer**
  - Automate the scheduling of Meraki Group Policies to restrict bandwidth or block specific categories/sites during designated family times.
  - Features: Override switch in HA, recurring schedules.
- **Scheduled Guest Key**
  - Periodically auto-generate a new Guest Wi-Fi IPSK and notify service workers or temporary staff via mobile app, email, or SMS.
  - Integration: Uses the `meraki_ha.create_guest_key` service.
- **Dead Node Auto-Heal**
  - Monitor the availability of Home Assistant entities representing downstream devices. If an entity goes unavailable for a set period, cycle the PoE power on the corresponding Meraki switch port to attempt a hardware reboot.
- **MT Sensor Threshold Alerts**
  - Pre-configured critical notification templates for Meraki MT sensors (Temperature, Humidity, Water Leak, Door/Window).
  - Includes: Throttling (don't spam), critical priority for water/heat.

## Custom Lovelace Cards (Dashboards)

- **Event Host QR Generator**
  - A dedicated card for generating and displaying Guest Wi-Fi credentials.
  - Features: Input field for name/duration, calls `meraki_ha.create_guest_key`, and renders a scanable QR code for easy connection.
- **Client Locator Glance Card**
  - Quickly search for a connected client by name or MAC address.
  - Displays: Parent Access Point, current RSSI/Signal strength, and connection duration.
- **Network Vitals Header**
  - A compact header for dashboards showing high-level network health.
  - Visuals: Mini traffic graphs, "health dots" for Gateway, Switches, and APs (Green/Yellow/Red).
- **Smart PoE Port Toggle**
  - A specialized list for Meraki switches that shows all ports.
  - Displays: Current power draw (W), port status, and a toggle to enable/disable PoE on that specific port.

## Native HA Entity Integrations

- **Native Firmware Management**
  - Allow users to view and trigger Meraki network upgrades natively from the HA UI via the `update` entity.
- **Edge Analytics & Presence**
  - Feed MV camera object detection (e.g., person/vehicle) directly into HA for instant automation triggers via the `binary_sensor` entity.
- **Network Device Tracking**
  - Use MR access point client associations for hyper-reliable, network-level presence tracking via the `device_tracker` entity.
- **PoE Port Control**
  - Expose MS switch ports as native toggles to easily bounce PoE power for locked-up smart home devices via the `switch` entity.
- **Dynamic Bandwidth Toggles**
  - Allow users to toggle specific SSIDs or Traffic Shaping rules via standard HA dashboards via the `select` or `switch` entity.
