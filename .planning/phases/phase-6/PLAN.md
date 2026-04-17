# Phase 6: Advanced Native Platforms

## Overview

Phase 6 focuses on deepening the integration with native Home Assistant platforms, specifically the `update` entity for firmware management and dedicated services for hardware maintenance (PoE power cycling).

## Objectives

1.  **Native Firmware Management:** Implement the `update` entity to surface available Meraki firmware versions and allow triggered upgrades.
2.  **PoE Power Cycling Service:** Add a dedicated service to "cycle" PoE power (bounce) on switch ports for hardware reboots.
3.  **MT Sensor Blueprint Expansion:** Expand existing blueprints to include templates specifically for the MT environmental sensor series.

## Success Criteria

1.  Users can see and trigger firmware updates natively in the HA UI.
2.  Hardware reboots via PoE power cycle work reliably through a dedicated service call.
3.  Critical MT sensor alerts (Leak, Temp) are easily automatable via pre-configured blueprints.

## Waves

- **Wave 1: Firmware Update Entity** (06-01-PLAN.md)
- **Wave 2: PoE Power Cycling Service** (06-02-PLAN.md)
- **Wave 3: MT Sensor Blueprints** (06-03-PLAN.md)
